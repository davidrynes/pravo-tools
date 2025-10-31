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
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import threading
import time
from datetime import datetime

# Import naší PDF merger třídy
try:
    from indesign_like_pdf_merger import InDesignLikePDFMerger
except ImportError:
    print("Chyba: Nelze importovat InDesignLikePDFMerger")
    sys.exit(1)

# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Vytvoření Flask aplikace
app = Flask(__name__)
app.config['SECRET_KEY'] = 'pdf-merger-web-app-2024'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

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
    
    def merge_files(self, file_pairs: list, rotation: int = -90) -> dict:
        """Spojí páry PDF souborů"""
        results = {
            'success': [],
            'errors': [],
            'total_files': len(file_pairs)
        }
        
        for i, pair in enumerate(file_pairs):
            try:
                # Extrakce názvů souborů z páru
                left_file = pair['left_file']
                right_file = pair['right_file']
                
                # Vytvoření názvu výstupního souboru
                left_page = self.parse_page_number(left_file)
                right_page = self.parse_page_number(right_file)
                output_name = f"merged_{left_page:02d}_{right_page:02d}_web.pdf"
                output_path = OUTPUT_FOLDER / output_name
                
                # Spojení souborů s dynamickou rotací podle pořadí stránek
                left_file_path = UPLOAD_FOLDER / left_file
                right_file_path = UPLOAD_FOLDER / right_file
                
                # Dynamická rotace pro oboustranný tisk
                # PŘEDNÍ STRANA (sudá-lichá): 2-3, 4-5, 6-7 → +90° (všechny stejně)
                # ZADNÍ STRANA (lichá-sudá): 3-4, 5-6, 7-8 → -90° (všechny opačně)
                if left_page % 2 == 0:  # Levá je sudá → Přední strana
                    rotation = 90
                    logger.info(f"Přední strana ({left_page}-{right_page}): Rotace +90°")
                else:  # Levá je lichá → Zadní strana
                    rotation = -90
                    logger.info(f"Zadní strana ({left_page}-{right_page}): Rotace -90°")
                
                success = self.merger.create_side_by_side_pdf_with_rotation(
                    left_file_path, right_file_path, output_path, rotation
                )
                
                if success:
                    file_size = output_path.stat().st_size / (1024 * 1024)  # MB
                    results['success'].append({
                        'filename': output_name,
                        'size_mb': round(file_size, 1),
                        'left_file': Path(left_file).name,
                        'right_file': Path(right_file).name
                    })
                else:
                    results['errors'].append(f"Chyba při spojování {left_file} + {right_file}")
                    
            except Exception as e:
                results['errors'].append(f"Chyba při zpracování páru {i+1}: {str(e)}")
        
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

@app.route('/api/auto-pair', methods=['POST'])
def auto_pair():
    """API endpoint pro automatické párování souborů"""
    try:
        files = web_merger.get_uploaded_files()
        pairs = []
        
        # Seskupení souborů podle čísel stránek
        page_groups = {}
        for file_path in files:
            page_num = web_merger.parse_page_number(file_path.name)
            if page_num not in page_groups:
                page_groups[page_num] = []
            page_groups[page_num].append(file_path)
        
        # Vytvoření párů
        for page_num in sorted(page_groups.keys()):
            if page_num % 2 == 0:  # Sudé číslo - levá stránka
                left_files = page_groups[page_num]
                right_page_num = page_num + 1
                
                if right_page_num in page_groups:
                    right_files = page_groups[right_page_num]
                    
                    # Vezme první soubor z každé skupiny
                    pairs.append({
                        'left_file': left_files[0].name,
                        'right_file': right_files[0].name,
                        'left_page': page_num,
                        'right_page': right_page_num
                    })
        
        return jsonify({
            'success': True,
            'pairs': pairs,
            'count': len(pairs)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/merge', methods=['POST'])
def merge_files():
    """API endpoint pro spojení PDF souborů"""
    global task_counter
    
    try:
        data = request.get_json()
        file_pairs = data.get('pairs', [])
        rotation = int(data.get('rotation', -90))
        
        if not file_pairs:
            return jsonify({
                'success': False,
                'error': 'Žádné páry souborů nebyly vybrány'
            })
        
        # Vytvoření úlohy
        task_counter += 1
        task_id = f"task_{task_counter}"
        
        processing_tasks[task_id] = {
            'status': 'processing',
            'progress': 0,
            'total': len(file_pairs),
            'completed': 0,
            'results': None,
            'start_time': time.time()
        }
        
        # Spuštění zpracování v samostatném vlákně
        def process_task():
            try:
                results = web_merger.merge_files(file_pairs, rotation)
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
            'message': 'Zpracování bylo spuštěno'
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
            return send_file(file_path, as_attachment=True)
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
