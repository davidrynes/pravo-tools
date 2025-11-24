#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Merger Web App - Webová aplikace pro spojování PDF souborů
Autor: David Rynes
Popis: Moderní webová aplikace s drag & drop podporou pro spojování PDF souborů
"""

import os
import sys
import json
import logging
import zipfile
import io
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, Response
from werkzeug.utils import secure_filename
import threading
import time
from datetime import datetime

# Import naší PDF merger třídy a pairing logiky
try:
    from indesign_like_pdf_merger import InDesignLikePDFMerger
    from pairing_logic import (
        get_pairing_key, 
        validate_pair, 
        auto_pair_files, 
        ensure_odd_on_right,
        PAIRING_KEYS
    )
except ImportError as e:
    print(f"Chyba: Nelze importovat moduly: {e}")
    sys.exit(1)

# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Vytvoření Flask aplikace
app = Flask(__name__)
app.config['SECRET_KEY'] = 'pdf-merger-web-app-2024'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max (pro až 80 souborů)

# Konfigurace složek
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('output')
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Globální proměnné pro sledování úloh
processing_tasks = {}
task_counter = 0

class WebPDFMerger:
    """Webová verze PDF merger třídy"""
    
    def __init__(self):
        self.merger = InDesignLikePDFMerger()
        self.merger.files_dir = UPLOAD_FOLDER
        self.merger.output_dir = OUTPUT_FOLDER
    
    def parse_page_number(self, filename: str) -> int:
        """
        Extrahuje číslo stránky z názvu souboru.
        
        Podporuje formáty:
        1. PRYYMMDDXXBBB.pdf - XX je na pozici -5:-3 (4. a 5. znak od konce)
        2. název_číslo.pdf - extrahuje číslo za poslední podtržítkem
        
        Příklady:
        - PR25103001VY1.pdf -> 01 (znaky na pozici -5:-3)
        - PR25103040VY1.pdf -> 40 (znaky na pozici -5:-3)
        - PRAVO_NEW_TEST03_FINAL_02.pdf -> 02 (fallback)
        - myfile_15.pdf -> 15 (fallback)
        """
        try:
            name = Path(filename).stem
            
            # Primární metoda: extrahujeme 4. a 5. znak od konce (před posledními 3 znaky)
            # Formát: PRYYMMDDXXBBB -> XX jsou na pozici [-5:-3]
            if len(name) >= 5:
                page_chars = name[-5:-3]
                if page_chars.isdigit():
                    return int(page_chars)
            
            # Fallback 1: zkusíme poslední 2 znaky
            if len(name) >= 2:
                last_two = name[-2:]
                if last_two.isdigit():
                    return int(last_two)
            
            # Fallback 2: zkusíme najít číslo za posledním podtržítkem
            parts = name.split('_')
            if parts:
                last_part = parts[-1]
                if last_part.isdigit():
                    return int(last_part)
            
            return 0
        except Exception as e:
            logger.warning(f"Chyba při parsování čísla stránky z '{filename}': {e}")
            return 0
    
    def get_uploaded_files(self) -> list:
        """Získá seznam nahraných PDF souborů"""
        pdf_files = list(UPLOAD_FOLDER.glob("*.pdf"))
        pdf_files.sort()
        return pdf_files
    
    def merge_files(self, file_pairs: list, day: str = "01", mutations: list = None, edition: str = "1") -> dict:
        """
        Spojí páry PDF souborů s jmennou konvencí pro tiskárnu.
        
        Jmenná konvence: 28PXE011.x.pdf
        - 28 = den vydání
        - PXE = kód mutace
        - 01 = číslo páru stran (nižší číslo ze dvojice)
        - 1 = číslo vydání
        - .x = CMYK (konstantní)
        """
        if mutations is None:
            mutations = ["PXB"]
        
        results = {
            'success': [],
            'errors': [],
            'total_files': len(file_pairs) * len(mutations)  # Počítáme s mutacemi
        }
        
        for i, pair in enumerate(file_pairs, start=1):  # start=1 pro 1-based pořadí
            try:
                # Extrakce názvů souborů z páru
                left_file = pair['left_file']
                right_file = pair['right_file']
                left_page = self.parse_page_number(left_file)
                right_page = self.parse_page_number(right_file)
                
                # ZAJIŠTĚNÍ: Liché strany vždy vpravo!
                # Pokud je levá stránka lichá, prohodíme
                if left_page % 2 == 1:  # Levá je lichá
                    left_file, right_file = right_file, left_file
                    left_page, right_page = right_page, left_page
                    logger.info(f"Pár přehozen: Liché ({right_page}) je nyní vpravo")
                
                # Číslo páru = nižší číslo strany ze dvojice
                pair_number = min(left_page, right_page)
                
                # Spojení souborů s rotací
                left_file_path = UPLOAD_FOLDER / left_file
                right_file_path = UPLOAD_FOLDER / right_file
                
                # OBOUSTRANNÝ TISK DVOJSTRAN:
                # - 1. pár = PŘEDNÍ strana papíru → -90°
                # - 2. pár = ZADNÍ strana papíru  → +90°
                # - 3. pár = PŘEDNÍ strana papíru → -90°
                # - 4. pár = ZADNÍ strana papíru  → +90°
                # Rotace závisí na POŘADÍ PÁRU (liché = přední, sudé = zadní)
                if i % 2 == 1:  # Liché pořadí (1, 3, 5...) = Přední strana
                    rotation = -90
                    side = "Přední"
                else:  # Sudé pořadí (2, 4, 6...) = Zadní strana
                    rotation = 90
                    side = "Zadní"
                
                logger.info(f"{i}. pár ({left_page}-{right_page}): {side} strana → Rotace {rotation}°")
                
                # Kontrola existence souborů
                if not left_file_path.exists():
                    error_msg = f"Levý soubor neexistuje: {left_file}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    continue
                    
                if not right_file_path.exists():
                    error_msg = f"Pravý soubor neexistuje: {right_file}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    continue
                
                # Pro každou mutaci vytvoříme kopii souboru
                for mutation in mutations:
                    # Jmenná konvence: 28PXE011.x.pdf
                    # {den}{mutace}{cislo_paru:02d}{cislo_vydani}.x.pdf
                    output_name = f"{day}{mutation}{pair_number:02d}{edition}.x.pdf"
                    output_path = OUTPUT_FOLDER / output_name
                    
                    logger.info(f"Vytvářím soubor: {output_name} (mutace {mutation})")
                    
                    # Pokus o merge s detailním logováním
                    try:
                        success = self.merger.create_side_by_side_pdf_with_rotation(
                            left_file_path, right_file_path, output_path, rotation
                        )
                        
                        if success:
                            if output_path.exists():
                                file_size = output_path.stat().st_size / (1024 * 1024)  # MB
                                results['success'].append({
                                    'filename': output_name,
                                    'size_mb': round(file_size, 1),
                                    'left_file': Path(left_file).name,
                                    'right_file': Path(right_file).name,
                                    'left_page': left_page,
                                    'right_page': right_page,
                                    'rotation': rotation,
                                    'pair_index': i,
                                    'mutation': mutation,
                                    'day': day,
                                    'edition': edition
                                })
                                logger.info(f"✅ Pár {i} ({mutation}) úspěšně sloučen: {output_name}")
                            else:
                                error_msg = f"Merge vrátil success, ale soubor neexistuje: {output_name}"
                                logger.error(error_msg)
                                results['errors'].append(error_msg)
                        else:
                            error_msg = f"Merge selhal (returned False): {left_file} + {right_file} ({mutation})"
                            logger.error(error_msg)
                            results['errors'].append(error_msg)
                    except Exception as merge_error:
                        error_msg = f"Exception při merge {left_file} + {right_file} ({mutation}): {str(merge_error)}"
                        logger.error(error_msg)
                        results['errors'].append(error_msg)
                    
            except Exception as e:
                error_msg = f"Chyba při zpracování páru {i}: {str(e)}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
        
        return results

# Globální instance
web_merger = WebPDFMerger()

@app.route('/')
def index():
    """Hlavní stránka"""
    return render_template('index.html')

@app.route('/api/files', methods=['GET'])
def get_files():
    """API endpoint pro získání seznamu nahraných souborů"""
    try:
        files = web_merger.get_uploaded_files()
        file_list = []
        
        for file_path in files:
            page_num = web_merger.parse_page_number(file_path.name)
            file_size = file_path.stat().st_size / (1024 * 1024)  # MB
            file_list.append({
                'name': file_path.name,
                'size_mb': round(file_size, 1),
                'page_number': page_num,
                'upload_time': datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%H:%M:%S')
            })
        
        return jsonify({
            'success': True,
            'files': file_list,
            'count': len(file_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """API endpoint pro nahrání souborů"""
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': 'Žádné soubory nebyly vybrány'})
        
        files = request.files.getlist('files')
        uploaded_files = []
        
        for file in files:
            if file and file.filename.lower().endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = UPLOAD_FOLDER / filename
                file.save(file_path)
                
                page_num = web_merger.parse_page_number(filename)
                file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                
                uploaded_files.append({
                    'name': filename,
                    'size_mb': round(file_size, 1),
                    'page_number': page_num
                })
        
        return jsonify({
            'success': True,
            'uploaded_files': uploaded_files,
            'message': f'Úspěšně nahráno {len(uploaded_files)} PDF souborů'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/page-counts', methods=['GET'])
def get_page_counts():
    """API endpoint pro získání podporovaných rozsahů vydání"""
    return jsonify({
        'success': True,
        'page_counts': list(PAIRING_KEYS.keys()),
        'default': 40
    })

@app.route('/api/validate-pair', methods=['POST'])
def validate_pair_endpoint():
    """API endpoint pro validaci páru"""
    try:
        data = request.get_json()
        left_page = int(data.get('left_page'))
        right_page = int(data.get('right_page'))
        page_count = int(data.get('page_count', 40))
        
        is_valid = validate_pair(left_page, right_page, page_count)
        
        if not is_valid:
            # Najdeme správný pár pro levou stránku
            pairing_key = get_pairing_key(page_count)
            correct_pair = None
            for l, r in pairing_key:
                if l == left_page:
                    correct_pair = r
                    break
                if r == left_page:
                    correct_pair = l
                    break
            
            return jsonify({
                'success': True,
                'valid': False,
                'message': f'Neplatný pár! Ke straně {left_page} patří strana {correct_pair}',
                'correct_pair': correct_pair
            })
        
        return jsonify({
            'success': True,
            'valid': True,
            'message': 'Platný pár'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/auto-pair', methods=['POST'])
def auto_pair():
    """API endpoint pro automatické párování souborů podle klíče"""
    try:
        data = request.get_json()
        page_count = int(data.get('page_count', 40))  # Výchozí 40 stran
        
        if page_count not in PAIRING_KEYS:
            return jsonify({
                'success': False,
                'error': f'Nepodporovaný rozsah vydání: {page_count}. Podporované: {list(PAIRING_KEYS.keys())}'
            })
        
        files = web_merger.get_uploaded_files()
        
        # Vytvoříme slovník page_number -> filename
        page_to_file = {}
        for file_path in files:
            page_num = web_merger.parse_page_number(file_path.name)
            if page_num > 0:
                page_to_file[page_num] = file_path.name
        
        # Získáme klíč párování pro daný rozsah
        pairing_key = get_pairing_key(page_count)
        
        # Vytvoříme páry podle klíče
        pairs = []
        for left_page, right_page in pairing_key:
            # Musíme mít obě stránky
            if left_page in page_to_file and right_page in page_to_file:
                pairs.append({
                    'left_file': page_to_file[left_page],
                    'right_file': page_to_file[right_page],
                    'left_page': left_page,
                    'right_page': right_page
                })
            else:
                logger.warning(f"Chybí stránka pro pár {left_page}-{right_page}")
        
        return jsonify({
            'success': True,
            'pairs': pairs,
            'count': len(pairs),
            'page_count': page_count,
            'message': f'Spárováno {len(pairs)} párů podle klíče pro {page_count} stran'
        })
        
    except Exception as e:
        logger.error(f"Chyba při auto-párování: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/merge', methods=['POST'])
def merge_files():
    """API endpoint pro spojení PDF souborů s parametry pro tiskárnu"""
    global task_counter
    
    try:
        data = request.get_json()
        file_pairs = data.get('pairs', [])
        day = data.get('day', '01')
        mutations = data.get('mutations', ['PXB'])
        edition = data.get('edition', '1')
        
        if not file_pairs:
            return jsonify({
                'success': False,
                'error': 'Žádné páry souborů nebyly vybrány'
            })
        
        logger.info(f"Export: den={day}, mutace={mutations}, vydání={edition}, párů={len(file_pairs)}")
        
        # Vytvoření úlohy
        task_counter += 1
        task_id = f"task_{task_counter}"
        
        # Počet výstupních souborů = páry × mutace
        total_files = len(file_pairs) * len(mutations)
        
        processing_tasks[task_id] = {
            'status': 'processing',
            'progress': 0,
            'total': total_files,
            'completed': 0,
            'results': None,
            'start_time': time.time()
        }
        
        # Spuštění zpracování v samostatném vlákně
        def process_task():
            try:
                results = web_merger.merge_files(file_pairs, day, mutations, edition)
                processing_tasks[task_id]['status'] = 'completed'
                processing_tasks[task_id]['results'] = results
                processing_tasks[task_id]['progress'] = 100
            except Exception as e:
                processing_tasks[task_id]['status'] = 'error'
                processing_tasks[task_id]['error'] = str(e)
        
        thread = threading.Thread(target=process_task)
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Export byl spuštěn'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """API endpoint pro získání stavu úlohy"""
    if task_id not in processing_tasks:
        return jsonify({
            'success': False,
            'error': 'Úloha nebyla nalezena'
        })
    
    task = processing_tasks[task_id]
    
    # Aktualizace progressu
    if task['status'] == 'processing':
        elapsed = time.time() - task['start_time']
        estimated_total = elapsed * task['total'] / max(task['completed'], 1)
        task['progress'] = min(int((task['completed'] / task['total']) * 100), 95)
    
    return jsonify({
        'success': True,
        'task': task
    })

@app.route('/api/download/<filename>')
def download_file(filename):
    """API endpoint pro stažení souboru"""
    try:
        file_path = OUTPUT_FOLDER / secure_filename(filename)
        if file_path.exists():
            # Odeslání souboru
            response = send_file(file_path, as_attachment=True)
            
            # Po odeslání smažeme soubor (pokud je query param auto_delete=true)
            auto_delete = request.args.get('auto_delete', 'false').lower() == 'true'
            if auto_delete:
                # Spuštíme smazání v samostatném vlákně po 2 sekundách
                def delete_after_download():
                    time.sleep(2)  # Počkáme než se soubor stáhne
                    try:
                        if file_path.exists():
                            file_path.unlink()
                            logger.info(f"Soubor {filename} byl automaticky smazán po stažení")
                    except Exception as e:
                        logger.error(f"Chyba při automatickém mazání souboru {filename}: {e}")
                
                thread = threading.Thread(target=delete_after_download)
                thread.daemon = True
                thread.start()
            
            return response
        else:
            return jsonify({'success': False, 'error': 'Soubor nebyl nalezen'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """API endpoint pro smazání souboru"""
    try:
        file_path = OUTPUT_FOLDER / secure_filename(filename)
        if file_path.exists():
            file_path.unlink()
            return jsonify({'success': True, 'message': 'Soubor byl smazán'})
        else:
            return jsonify({'success': False, 'error': 'Soubor nebyl nalezen'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/clear', methods=['POST'])
def clear_files():
    """API endpoint pro vyčištění všech souborů"""
    try:
        # Smazání nahraných souborů
        for file_path in UPLOAD_FOLDER.glob("*.pdf"):
            file_path.unlink()
        
        # Smazání výstupních souborů
        for file_path in OUTPUT_FOLDER.glob("*.pdf"):
            file_path.unlink()
        
        return jsonify({
            'success': True,
            'message': 'Všechny soubory byly smazány'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/download-all', methods=['POST'])
def download_all_files():
    """API endpoint pro stažení všech výstupních souborů jako ZIP"""
    try:
        data = request.get_json()
        filenames = data.get('filenames', [])
        
        if not filenames:
            return jsonify({
                'success': False,
                'error': 'Žádné soubory ke stažení'
            })
        
        # Vytvoření ZIP archivu v paměti
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename in filenames:
                file_path = OUTPUT_FOLDER / secure_filename(filename)
                if file_path.exists():
                    zf.write(file_path, filename)
                    logger.info(f"Přidán do ZIP: {filename}")
        
        memory_file.seek(0)
        
        # Generování názvu ZIP souboru
        today = datetime.now().strftime('%Y-%m-%d')
        zip_filename = f"pary_{today}.zip"
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_filename
        )
        
    except Exception as e:
        logger.error(f"Chyba při vytváření ZIP: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/clear-results', methods=['POST'])
def clear_results():
    """API endpoint pro smazání výstupních souborů (výsledků exportu)"""
    try:
        deleted_count = 0
        for file_path in OUTPUT_FOLDER.glob("*.pdf"):
            file_path.unlink()
            deleted_count += 1
            logger.info(f"Smazán: {file_path.name}")
        
        # Smazání i ZIP souborů
        for file_path in OUTPUT_FOLDER.glob("*.zip"):
            file_path.unlink()
            deleted_count += 1
        
        return jsonify({
            'success': True,
            'message': f'Smazáno {deleted_count} souborů',
            'deleted_count': deleted_count
        })
    except Exception as e:
        logger.error(f"Chyba při mazání výsledků: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("=== PDF Merger Web App ===")
    print("Spouštím webovou aplikaci...")
    
    # Pro lokální vývoj
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RENDER'):
        # Produkční prostředí
        port = int(os.environ.get('PORT', 8080))
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        # Lokální vývoj
        print("Otevřete prohlížeč na adrese: http://localhost:8080")
        print("Pro ukončení stiskněte Ctrl+C")
        app.run(debug=True, host='0.0.0.0', port=8080)
