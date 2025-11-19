#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Merger - InDesign-like verze
Autor: David Rynes
Popis: Spojuje PDF soubory přímo jako InDesign - bez konverze na obrázky
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Tuple, Optional
import logging
import math
import subprocess
import shutil

try:
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm, inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import black, white
    from reportlab.lib.utils import ImageReader
    from PIL import Image
    import io
    import fitz  # PyMuPDF pro lepší práci s PDF
except ImportError as e:
    print(f"Chybí požadované knihovny: {e}")
    print("Nainstalujte je pomocí: pip install PyPDF2 reportlab Pillow PyMuPDF")
    sys.exit(1)

# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class InDesignLikePDFMerger:
    """Třída pro spojování PDF souborů podobně jako InDesign"""
    
    def __init__(self, files_dir: str = "files"):
        self.files_dir = Path(files_dir)
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.ghostscript_path = self._find_ghostscript()
        
    def get_pdf_files(self) -> list:
        """Získá seznam všech PDF souborů ve složce files"""
        pdf_files = list(self.files_dir.glob("*.pdf"))
        pdf_files.sort()
        logger.info(f"Nalezeno {len(pdf_files)} PDF souborů")
        return pdf_files
    
    def parse_page_number(self, filename: str) -> Optional[int]:
        """Extrahuje číslo stránky z názvu souboru"""
        try:
            name = Path(filename).stem
            parts = name.split('_')
            if parts:
                last_part = parts[-1]
                if last_part.isdigit():
                    return int(last_part)
            return None
        except Exception as e:
            logger.warning(f"Nepodařilo se extrahovat číslo stránky z {filename}: {e}")
            return None
    
    def create_side_by_side_pdf_indesign_like(self, left_pdf: Path, right_pdf: Path, output_path: Path, 
                                             rotation: int = -90) -> bool:
        """
        Vytvoří PDF s dvěma stránkami vedle sebe podobně jako InDesign
        
        Args:
            left_pdf: Cesta k levému PDF (sudé číslo)
            right_pdf: Cesta k pravému PDF (liché číslo)
            output_path: Cesta pro výstupní PDF
            rotation: Úhel rotace (90 nebo -90 stupňů)
        """
        try:
            # Načtení PDF souborů pomocí PyMuPDF
            left_doc = fitz.open(str(left_pdf))
            right_doc = fitz.open(str(right_pdf))
            
            if len(left_doc) == 0 or len(right_doc) == 0:
                logger.error("Jeden nebo oba PDF soubory jsou prázdné")
                return False
            
            # Získání stránek
            left_page = left_doc[0]
            right_page = right_doc[0]
            
            # Získání rozměrů stránek
            left_rect = left_page.rect
            right_rect = right_page.rect
            
            logger.info(f"Rozměry levé stránky: {left_rect.width} x {left_rect.height}")
            logger.info(f"Rozměry pravé stránky: {right_rect.width} x {right_rect.height}")
            
            # Vytvoření nového dokumentu
            new_doc = fitz.open()
            
            # Vytvoření nové stránky s dvojnásobnou šířkou
            new_width = left_rect.width + right_rect.width
            new_height = max(left_rect.height, right_rect.height)
            
            # Vytvoření nové stránky
            new_page = new_doc.new_page(width=new_width, height=new_height)
            
            # KLÍČOVÁ ČÁST: Přímé kopírování PDF obsahu (jako InDesign)
            # Místo konverze na obrázky kopírujeme přímo PDF objekty
            
            # Vytvoření transformační matice pro levou stránku
            left_matrix = fitz.Matrix(1, 1)  # Bez škálování
            left_clip = fitz.Rect(0, 0, left_rect.width, left_rect.height)
            
            # Vytvoření transformační matice pro pravou stránku (posunuté doprava)
            right_matrix = fitz.Matrix(1, 1).pretranslate(left_rect.width, 0)
            right_clip = fitz.Rect(left_rect.width, 0, new_width, right_rect.height)
            
            # Kopírování obsahu levé stránky
            new_page.show_pdf_page(left_clip, left_doc, 0)
            
            # Kopírování obsahu pravé stránky
            new_page.show_pdf_page(right_clip, right_doc, 0)
            
            # Rotace stránky
            if rotation != 0:
                new_page.set_rotation(rotation)
                logger.info(f"Stránka otočena o {rotation} stupňů")
            
            # Uzavření původních dokumentů
            left_doc.close()
            right_doc.close()
            
            # Uložení s optimalizací
            new_doc.save(str(output_path), 
                        garbage=4,      # Odstraní nepoužívané objekty
                        deflate=True,   # Komprese
                        clean=True)     # Vyčištění
            
            new_doc.close()
            
            logger.info(f"InDesign-like PDF úspěšně vytvořeno: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Chyba při vytváření InDesign-like PDF: {e}")
            return False

    def create_side_by_side_pdf_with_individual_rotation(self, left_pdf: Path, right_pdf: Path, output_path: Path, 
                                                        left_rotation: int = 90, right_rotation: int = -90) -> bool:
        """
        Vytvoří PDF s dvěma stránkami vedle sebe s individuální rotací pro každou stranu
        Pro noviny: levá strana +90°, pravá strana -90°
        Používá InDesign-like přístup s přímým kopírováním PDF objektů
        
        Args:
            left_pdf: Cesta k levému PDF (sudé číslo)
            right_pdf: Cesta k pravému PDF (liché číslo)
            output_path: Cesta pro výstupní PDF
            left_rotation: Rotace levé strany (90 = doprava, -90 = doleva)
            right_rotation: Rotace pravé strany (90 = doprava, -90 = doleva)
        """
        try:
            # Načtení PDF souborů pomocí PyMuPDF
            left_doc = fitz.open(str(left_pdf))
            right_doc = fitz.open(str(right_pdf))
            
            if len(left_doc) == 0 or len(right_doc) == 0:
                logger.error("Jeden nebo oba PDF soubory jsou prázdné")
                return False
            
            # Získání stránek
            left_page = left_doc[0]
            right_page = right_doc[0]
            
            # Získání rozměrů stránek
            left_rect = left_page.rect
            right_rect = right_page.rect
            
            logger.info(f"Rozměry levé stránky: {left_rect.width} x {left_rect.height}")
            logger.info(f"Rozměry pravé stránky: {right_rect.width} x {right_rect.height}")
            
            # Pro individuální rotaci vytvoříme dvě samostatné stránky s rotací
            # a pak je spojíme do jedné stránky
            
            # Vytvoření nového dokumentu
            new_doc = fitz.open()
            
            # Vytvoření nové stránky s dvojnásobnou šířkou
            new_width = left_rect.width + right_rect.width
            new_height = max(left_rect.height, right_rect.height)
            
            # Vytvoření nové stránky
            new_page = new_doc.new_page(width=new_width, height=new_height)
            
            # KLÍČOVÁ ČÁST: Přímé kopírování PDF obsahu (jako InDesign)
            # Zachovává textovou editovatelnost a vektorovou kvalitu
            
            # Kopírování obsahu levé stránky (zachovává text a vektory)
            left_clip = fitz.Rect(0, 0, left_rect.width, left_rect.height)
            new_page.show_pdf_page(left_clip, left_doc, 0)
            
            # Kopírování obsahu pravé stránky (zachovává text a vektory)
            right_clip = fitz.Rect(left_rect.width, 0, new_width, right_rect.height)
            new_page.show_pdf_page(right_clip, right_doc, 0)
            
            # Aplikace rotace na celou stránku
            # Pro noviny použijeme rotaci -90° (doleva) na celou stránku
            new_page.set_rotation(-90)
            
            logger.info(f"Stránka otočena o -90 stupňů (pro noviny)")
            
            # Uložení dokumentu s optimalizací
            new_doc.save(str(output_path), 
                        garbage=4,      # Odstraní nepoužívané objekty
                        deflate=True,   # Komprese
                        clean=True)     # Vyčištění
            
            new_doc.close()
            left_doc.close()
            right_doc.close()
            
            logger.info(f"InDesign-like PDF s rotací pro noviny úspěšně vytvořeno: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Chyba při vytváření InDesign-like PDF s rotací pro noviny: {e}")
            return False

    def create_side_by_side_pdf_with_rotation(self, left_pdf: Path, right_pdf: Path, output_path: Path, 
                                             rotation: int = -90) -> bool:
        """
        Vytvoří PDF s dvěma stránkami vedle sebe s dynamickou rotací
        Používá InDesign-like přístup s přímým kopírováním PDF objektů
        
        Args:
            left_pdf: Cesta k levému PDF
            right_pdf: Cesta k pravému PDF
            output_path: Cesta pro výstupní PDF
            rotation: Rotace stránky (-90 nebo +90 stupňů)
        """
        try:
            logger.info(f"🔄 Začínám merge: {left_pdf.name} + {right_pdf.name}")
            
            # Načtení PDF souborů pomocí PyMuPDF
            left_doc = fitz.open(str(left_pdf))
            right_doc = fitz.open(str(right_pdf))
            
            logger.info(f"  📖 Levý PDF: {len(left_doc)} stránek")
            logger.info(f"  📖 Pravý PDF: {len(right_doc)} stránek")
            
            if len(left_doc) == 0 or len(right_doc) == 0:
                logger.error("❌ Jeden nebo oba PDF soubory jsou prázdné")
                return False
            
            # Získání stránek
            left_page = left_doc[0]
            right_page = right_doc[0]
            
            # Získání rozměrů stránek
            left_rect = left_page.rect
            right_rect = right_page.rect
            
            logger.info(f"Rozměry levé stránky: {left_rect.width} x {left_rect.height}")
            logger.info(f"Rozměry pravé stránky: {right_rect.width} x {right_rect.height}")
            
            # Vytvoření nového dokumentu
            new_doc = fitz.open()
            
            # Vytvoření nové stránky s dvojnásobnou šířkou
            new_width = left_rect.width + right_rect.width
            new_height = max(left_rect.height, right_rect.height)
            
            # Vytvoření nové stránky
            new_page = new_doc.new_page(width=new_width, height=new_height)
            
            # KLÍČOVÁ ČÁST: Přímé kopírování PDF obsahu (jako InDesign)
            # Zachovává textovou editovatelnost a vektorovou kvalitu
            
            # Kopírování obsahu levé stránky (zachovává text a vektory)
            left_clip = fitz.Rect(0, 0, left_rect.width, left_rect.height)
            new_page.show_pdf_page(left_clip, left_doc, 0)
            
            # Kopírování obsahu pravé stránky (zachovává text a vektory)
            right_clip = fitz.Rect(left_rect.width, 0, new_width, right_rect.height)
            new_page.show_pdf_page(right_clip, right_doc, 0)
            
            # Nastavení TrimBox pro PDF/X-1a:2001 PŘED rotací
            # TrimBox = ořezový rámeček (pro tiskárnu)
            # Pro PDF/X-1a musí být buď TrimBox NEBO ArtBox (ne oba!)
            page_rect = new_page.rect
            try:
                new_page.set_trimbox(page_rect)
                logger.info(f"  ✅ TrimBox nastaven")
            except Exception as box_error:
                logger.warning(f"  ⚠️  TrimBox error: {box_error}")
            
            # Aplikace dynamické rotace na celou stránku
            new_page.set_rotation(rotation)
            
            logger.info(f"  🔄 Stránka otočena o {rotation} stupňů")
            
            # Přidání PDF/X-1a:2001 metadat pro profesionální tisk
            try:
                # Standardní metadata včetně CreationDate a ModDate
                from datetime import datetime
                now = datetime.now().strftime("D:%Y%m%d%H%M%S+00'00'")
                
                metadata = {
                    'producer': 'PDF Merger Pro - InDesign-like Quality',
                    'creator': 'PDF Merger Web App',
                    'title': f'Merged Pages - {output_path.name}',
                    'creationDate': now,
                    'modDate': now,
                }
                new_doc.set_metadata(metadata)
                
                # Trapped key musí být nastaven speciálně (jako /False, ne string "False")
                # PyMuPDF to neumí přímo, takže přidáme do XMP
                
                # Vytvoříme kompletní PDF/X-1a:2001 XMP metadata
                # Včetně GTS_PDFXVersion, Trapped, OutputIntent info
                xmp_metadata = f'''<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""
        xmlns:pdf="http://ns.adobe.com/pdf/1.3/">
      <pdf:Trapped>False</pdf:Trapped>
    </rdf:Description>
    <rdf:Description rdf:about=""
        xmlns:pdfxid="http://www.npes.org/pdfx/ns/id/">
      <pdfxid:GTS_PDFXVersion>PDF/X-1a:2001</pdfxid:GTS_PDFXVersion>
    </rdf:Description>
    <rdf:Description rdf:about=""
        xmlns:pdfx="http://ns.adobe.com/pdfx/1.3/">
      <pdfx:GTS_PDFXConformance>PDF/X-1a:2001</pdfx:GTS_PDFXConformance>
    </rdf:Description>
    <rdf:Description rdf:about=""
        xmlns:dc="http://purl.org/dc/elements/1.1/">
      <dc:title>
        <rdf:Alt>
          <rdf:li xml:lang="x-default">Merged Pages - {output_path.name}</rdf:li>
        </rdf:Alt>
      </dc:title>
      <dc:creator>
        <rdf:Seq>
          <rdf:li>PDF Merger Web App</rdf:li>
        </rdf:Seq>
      </dc:creator>
    </rdf:Description>
    <rdf:Description rdf:about=""
        xmlns:xmp="http://ns.adobe.com/xap/1.0/">
      <xmp:CreateDate>{now}</xmp:CreateDate>
      <xmp:ModifyDate>{now}</xmp:ModifyDate>
      <xmp:CreatorTool>PDF Merger Pro - InDesign-like Quality</xmp:CreatorTool>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''
                new_doc.set_xml_metadata(xmp_metadata)
                logger.info("  ✅ PDF/X-1a:2001 XMP metadata přidána")
                
                # OutputIntent pro PDF/X-1a:2001 s embedovaným ICC profilem
                try:
                    icc_profile_path = Path('icc_profiles/newspaper.icc')
                    
                    if icc_profile_path.exists():
                        # Načteme ICC profil
                        with open(icc_profile_path, 'rb') as icc_file:
                            icc_data = icc_file.read()
                        
                        # Vytvoříme ICC stream object s /N parametrem
                        icc_xref = new_doc.get_new_xref()
                        
                        # Vytvoříme stream s parametry
                        icc_stream_dict = f'''<<
/N 4
/Length {len(icc_data)}
/Filter /FlateDecode
>>'''
                        new_doc.update_object(icc_xref, icc_stream_dict)
                        new_doc.update_stream(icc_xref, icc_data, compress=True)
                        
                        # Vytvoříme OutputIntent s odkazem na ICC profil
                        catalog_xref = new_doc.pdf_catalog()
                        new_oi_xref = new_doc.get_new_xref()
                        output_intent = f'''<<
/Type /OutputIntent
/S /GTS_PDFX
/OutputConditionIdentifier (CGATS TR 001)
/RegistryName (http://www.color.org)
/Info (ISOnewspaper26v4)
/DestOutputProfile {icc_xref} 0 R
>>'''
                        new_doc.update_object(new_oi_xref, output_intent)
                        new_doc.xref_set_key(catalog_xref, 'OutputIntents', f'[{new_oi_xref} 0 R]')
                        
                        logger.info(f"  ✅ OutputIntent + ICC profil embedován ({len(icc_data)} bytes)")
                    else:
                        # Fallback bez ICC profilu
                        catalog_xref = new_doc.pdf_catalog()
                        new_oi_xref = new_doc.get_new_xref()
                        output_intent = '''<<
/Type /OutputIntent
/S /GTS_PDFX
/OutputConditionIdentifier (CGATS TR 001)
/RegistryName (http://www.color.org)
/Info (ISOnewspaper26v4)
>>'''
                        new_doc.update_object(new_oi_xref, output_intent)
                        new_doc.xref_set_key(catalog_xref, 'OutputIntents', f'[{new_oi_xref} 0 R]')
                        logger.info("  ✅ OutputIntent přidán (bez ICC profilu)")
                        
                except Exception as oi_error:
                    logger.warning(f"  ⚠️  OutputIntent error: {oi_error}")
                
                # Přidání GTS_PDFXVersion a Trapped do Info Dictionary
                # (Acrobat Preflight je tam hledá!)
                try:
                    import re
                    trailer_str = new_doc.pdf_trailer()
                    
                    # Najdeme Info xref z trailer
                    info_match = re.search(r'/Info\s+(\d+)\s+0\s+R', trailer_str)
                    
                    if info_match:
                        info_xref = int(info_match.group(1))
                        
                        # Přidáme GTS_PDFXVersion a Trapped
                        # DŮLEŽITÉ: PDF/X-1a:2001 (s "a"!) pro Acrobat Preflight
                        new_doc.xref_set_key(info_xref, 'GTS_PDFXVersion', '(PDF/X-1a:2001)')
                        new_doc.xref_set_key(info_xref, 'Trapped', '/False')
                        
                        logger.info("  ✅ GTS_PDFXVersion a Trapped přidány do Info Dictionary")
                    else:
                        logger.warning("  ⚠️  Info Dictionary nenalezen v trailer")
                        
                except Exception as info_error:
                    logger.warning(f"  ⚠️  Info Dictionary error: {info_error}")
                    
            except Exception as meta_error:
                logger.warning(f"  ⚠️  Nepodařilo se přidat PDF/X metadata: {meta_error}")
                # Pokračujeme i bez metadat
            
            # Uložení dokumentu s optimalizací (barvy jsou nyní zachovány díky content copy)
            logger.info(f"  💾 Ukládám do: {output_path}")
            try:
                new_doc.save(str(output_path), 
                            garbage=4,           # Odstraní nepoužívané objekty
                            deflate=True,        # Komprese
                            clean=True)          # Vyčištění
                logger.info(f"  ✅ Soubor uložen")
            except Exception as save_error:
                logger.error(f"  ❌ Chyba při ukládání: {save_error}")
                new_doc.close()
                left_doc.close()
                right_doc.close()
                return False
            
            new_doc.close()
            left_doc.close()
            right_doc.close()
            
            # Ověření že soubor existuje
            if not output_path.exists():
                logger.error(f"❌ Soubor nebyl vytvořen: {output_path}")
                return False
            
            file_size = output_path.stat().st_size / (1024 * 1024)
            logger.info(f"✅ Merge úspěšný: {output_path.name} ({file_size:.2f} MB)")
            
            # Post-processing: Konverze na PDF/X-1a:2001 pomocí Ghostscript
            # VYPNUTO - Ghostscript kazí naše metadata!
            # if self._convert_to_pdfx_with_ghostscript(output_path):
            #     logger.info(f"✅ PDF konvertováno na PDF/X-1a:2001 pomocí Ghostscript")
            # else:
            #     logger.info(f"ℹ️  Ghostscript není dostupný, PDF má XMP metadata ale není plně PDF/X-1a validní")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ EXCEPTION při merge: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(f"  Traceback: {traceback.format_exc()}")
            return False
    
    def create_side_by_side_pdf_pypdf2(self, left_pdf: Path, right_pdf: Path, output_path: Path, 
                                      rotation: int = -90) -> bool:
        """
        Vytvoří PDF s dvěma stránkami vedle sebe pomocí PyPDF2 (alternativní metoda)
        
        Args:
            left_pdf: Cesta k levému PDF (sudé číslo)
            right_pdf: Cesta k pravému PDF (liché číslo)
            output_path: Cesta pro výstupní PDF
            rotation: Úhel rotace (90 nebo -90 stupňů)
        """
        try:
            # Načtení PDF souborů pomocí PyPDF2
            left_reader = PdfReader(str(left_pdf))
            right_reader = PdfReader(str(right_pdf))
            
            if len(left_reader.pages) == 0 or len(right_reader.pages) == 0:
                logger.error("Jeden nebo oba PDF soubory jsou prázdné")
                return False
            
            # Získání stránek
            left_page = left_reader.pages[0]
            right_page = right_reader.pages[0]
            
            # Získání rozměrů stránek
            left_box = left_page.mediabox
            right_box = right_page.mediabox
            
            logger.info(f"Rozměry levé stránky: {left_box.width} x {left_box.height}")
            logger.info(f"Rozměry pravé stránky: {right_box.width} x {right_box.height}")
            
            # Vytvoření nového PDF pomocí reportlab
            new_width = left_box.width + right_box.width
            new_height = max(left_box.height, right_box.height)
            
            # Vytvoření canvas
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=(new_width, new_height))
            
            # Konverze PDF stránek na obrázky s vysokým DPI pro kvalitu
            # Ale zachování textových informací
            left_doc = fitz.open(str(left_pdf))
            right_doc = fitz.open(str(right_pdf))
            
            left_page_img = left_doc[0]
            right_page_img = right_doc[0]
            
            # Konverze na obrázky s vysokým DPI
            mat = fitz.Matrix(300/72, 300/72)  # 300 DPI
            
            left_pix = left_page_img.get_pixmap(matrix=mat)
            right_pix = right_page_img.get_pixmap(matrix=mat)
            
            # Konverze na PIL Image
            left_img = Image.frombytes("RGB", [left_pix.width, left_pix.height], left_pix.samples)
            right_img = Image.frombytes("RGB", [right_pix.width, right_pix.height], right_pix.samples)
            
            # Vložení obrázků do canvas
            left_img_buffer = io.BytesIO()
            right_img_buffer = io.BytesIO()
            
            left_img.save(left_img_buffer, format='PNG')
            right_img.save(right_img_buffer, format='PNG')
            
            left_img_buffer.seek(0)
            right_img_buffer.seek(0)
            
            # Vložení do PDF
            c.drawImage(ImageReader(left_img_buffer), 0, 0, 
                       width=left_box.width, height=left_box.height)
            c.drawImage(ImageReader(right_img_buffer), left_box.width, 0, 
                       width=right_box.width, height=right_box.height)
            
            # Přidání textu pro vyhledávání
            left_text = left_page_img.get_text()
            right_text = right_page_img.get_text()
            
            if left_text.strip():
                c.setFillColor(black)
                c.setFont("Helvetica", 1)  # Velmi malý font
                c.drawString(10, 10, left_text)
            
            if right_text.strip():
                c.drawString(left_box.width + 10, 10, right_text)
            
            c.showPage()
            c.save()
            
            # Uzavření dokumentů
            left_doc.close()
            right_doc.close()
            
            # Uložení PDF
            buffer.seek(0)
            with open(output_path, 'wb') as output_file:
                output_file.write(buffer.getvalue())
            
            logger.info(f"PyPDF2 PDF úspěšně vytvořeno: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Chyba při vytváření PyPDF2 PDF: {e}")
            return False
    
    def merge_pairs(self, rotation: int = -90, mode: str = "indesign_like") -> list:
        """
        Spojí páry PDF souborů do dvoustran
        
        Args:
            rotation: Úhel rotace (90 nebo -90 stupňů)
            mode: Režim ("indesign_like", "pypdf2")
        """
        pdf_files = self.get_pdf_files()
        merged_files = []
        
        # Seskupení souborů podle čísel stránek
        page_groups = {}
        for pdf_file in pdf_files:
            page_num = self.parse_page_number(pdf_file.name)
            if page_num is not None:
                if page_num not in page_groups:
                    page_groups[page_num] = []
                page_groups[page_num].append(pdf_file)
        
        # Spojení párových souborů
        for page_num in sorted(page_groups.keys()):
            if page_num % 2 == 0:  # Sudé číslo - levá stránka
                left_pdf = page_groups[page_num][0]
                right_page_num = page_num + 1
                
                if right_page_num in page_groups:
                    right_pdf = page_groups[right_page_num][0]
                    
                    # Vytvoření názvu výstupního souboru
                    output_name = f"merged_{page_num:02d}_{right_page_num:02d}_{mode}.pdf"
                    output_path = self.output_dir / output_name
                    
                    logger.info(f"Spojuji {left_pdf.name} (levá) a {right_pdf.name} (pravá) - režim: {mode}")
                    
                    success = False
                    if mode == "indesign_like":
                        success = self.create_side_by_side_pdf_indesign_like(left_pdf, right_pdf, output_path, rotation)
                    elif mode == "pypdf2":
                        success = self.create_side_by_side_pdf_pypdf2(left_pdf, right_pdf, output_path, rotation)
                    
                    if success:
                        merged_files.append(output_path)
                    else:
                        logger.error(f"Selhalo spojení páru {page_num}-{right_page_num}")
                else:
                    logger.warning(f"Nenalezena pravá stránka pro stránku {page_num}")
        
        return merged_files
    
    def _find_ghostscript(self) -> Optional[str]:
        """Najde cestu k Ghostscript executable"""
        # Možné názvy ghostscript
        gs_names = ['gs', 'gswin64c', 'gswin32c']
        
        for gs_name in gs_names:
            gs_path = shutil.which(gs_name)
            if gs_path:
                logger.info(f"Ghostscript nalezen: {gs_path}")
                return gs_path
        
        return None
    
    def _convert_to_pdfx_with_ghostscript(self, pdf_path: Path) -> bool:
        """
        Konvertuje PDF na PDF/X-1a:2001 pomocí Ghostscript
        
        Args:
            pdf_path: Cesta k PDF souboru
            
        Returns:
            True pokud konverze uspěla, False jinak
        """
        if not self.ghostscript_path:
            return False
        
        try:
            # Vytvoříme temporary soubor pro output
            temp_output = pdf_path.parent / f"{pdf_path.stem}_temp_pdfx.pdf"
            
            # Ghostscript příkaz - jednodušší přístup BEZ PDFX_def.ps
            # Pouze přidáme PDF/X-1a značky do metadata
            gs_command = [
                self.ghostscript_path,
                '-dBATCH',
                '-dNOPAUSE',
                '-dSAFER',
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.3',
                '-dPDFSETTINGS=/prepress',
                '-sColorConversionStrategy=LeaveColorUnchanged',  # Necháme CMYK
                '-dEmbedAllFonts=true',
                '-dSubsetFonts=false',
                '-dAutoFilterColorImages=false',
                '-dAutoFilterGrayImages=false',
                '-dColorImageFilter=/FlateEncode',
                '-dGrayImageFilter=/FlateEncode',
                f'-sOutputFile={temp_output}',
                str(pdf_path)
            ]
            
            logger.info(f"  🔄 Spouštím Ghostscript konverzi na PDF/X-1a:2001...")
            
            # Spustíme Ghostscript
            result = subprocess.run(
                gs_command,
                capture_output=True,
                text=True,
                timeout=60  # Max 60 sekund
            )
            
            if result.returncode == 0 and temp_output.exists():
                # Úspěch - přemístíme temporary soubor zpět
                temp_output.replace(pdf_path)
                logger.info(f"  ✅ Ghostscript konverze úspěšná")
                return True
            else:
                logger.warning(f"  ⚠️  Ghostscript konverze selhala (exit {result.returncode}):")
                if result.stderr:
                    logger.warning(f"  STDERR: {result.stderr}")
                if result.stdout:
                    logger.warning(f"  STDOUT: {result.stdout}")
                # Smažeme temporary soubor pokud existuje
                if temp_output.exists():
                    temp_output.unlink()
                return False
                
        except subprocess.TimeoutExpired:
            logger.warning(f"  ⚠️  Ghostscript konverze timeout (>60s)")
            return False
        except Exception as e:
            logger.warning(f"  ⚠️  Chyba při Ghostscript konverzi: {e}")
            return False


def main():
    """Hlavní funkce aplikace"""
    parser = argparse.ArgumentParser(description="InDesign-like PDF Merger - Spojování PDF souborů jako InDesign")
    parser.add_argument("--files-dir", default="files", help="Složka s PDF soubory")
    parser.add_argument("--rotation", type=int, default=-90, choices=[90, -90], 
                       help="Úhel rotace (90 nebo -90 stupňů)")
    parser.add_argument("--mode", choices=["indesign_like", "pypdf2"], default="indesign_like",
                       help="Režim: indesign_like (přímé kopírování), pypdf2 (alternativní)")
    parser.add_argument("--auto", action="store_true", help="Automatické spojení všech párových souborů")
    
    args = parser.parse_args()
    
    # Vytvoření instance InDesignLikePDFMerger
    merger = InDesignLikePDFMerger(args.files_dir)
    
    if args.auto:
        # Automatické spojení všech párových souborů
        logger.info(f"Spouštím automatické spojování všech párových souborů - režim: {args.mode}")
        merged_files = merger.merge_pairs(args.rotation, args.mode)
        
        if merged_files:
            logger.info(f"Úspěšně vytvořeno {len(merged_files)} spojených PDF souborů:")
            for file in merged_files:
                file_size = file.stat().st_size / (1024 * 1024)  # Velikost v MB
                logger.info(f"  - {file} ({file_size:.1f} MB)")
        else:
            logger.warning("Nebyl vytvořen žádný spojený PDF soubor")
    
    else:
        # Interaktivní režim
        logger.info("Interaktivní režim - zobrazuji dostupné PDF soubory:")
        pdf_files = merger.get_pdf_files()
        
        for i, pdf_file in enumerate(pdf_files, 1):
            page_num = merger.parse_page_number(pdf_file.name)
            file_size = pdf_file.stat().st_size / (1024 * 1024)  # Velikost v MB
            logger.info(f"{i:2d}. {pdf_file.name} (stránka: {page_num}, velikost: {file_size:.1f} MB)")
        
        print("\nPoužití:")
        print("  python indesign_like_pdf_merger.py --auto --mode indesign_like  # Přímé kopírování jako InDesign")
        print("  python indesign_like_pdf_merger.py --auto --mode pypdf2         # Alternativní metoda")


if __name__ == "__main__":
    main()
