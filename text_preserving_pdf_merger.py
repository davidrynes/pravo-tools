#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Merger - Verze s zachováním textu
Autor: David Rynes
Popis: Spojuje PDF soubory s zachováním textových informací pro vyhledávání a kopírování
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Tuple, Optional
import logging
import math

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


class TextPreservingPDFMerger:
    """Třída pro spojování PDF souborů s zachováním textových informací"""
    
    def __init__(self, files_dir: str = "files"):
        self.files_dir = Path(files_dir)
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
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
    
    def create_side_by_side_pdf_with_text(self, left_pdf: Path, right_pdf: Path, output_path: Path, 
                                        rotation: int = -90, dpi: int = 300) -> bool:
        """
        Vytvoří PDF s dvěma stránkami vedle sebe s zachováním textových informací
        
        Args:
            left_pdf: Cesta k levému PDF (sudé číslo)
            right_pdf: Cesta k pravému PDF (liché číslo)
            output_path: Cesta pro výstupní PDF
            rotation: Úhel rotace (90 nebo -90 stupňů)
            dpi: DPI pro tiskárny (300 je standardní)
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
            
            # Konverze stránek na obrázky s vysokým DPI pro kvalitu
            mat = fitz.Matrix(dpi/72, dpi/72)  # Profesionální DPI (300)
            
            left_pix = left_page.get_pixmap(matrix=mat)
            right_pix = right_page.get_pixmap(matrix=mat)
            
            # Vložení obrázků
            left_img_rect = fitz.Rect(0, 0, left_rect.width, left_rect.height)
            right_img_rect = fitz.Rect(left_rect.width, 0, new_width, right_rect.height)
            
            new_page.insert_image(left_img_rect, pixmap=left_pix)
            new_page.insert_image(right_img_rect, pixmap=right_pix)
            
            # KLÍČOVÁ ČÁST: Zachování textových informací
            # Získání textu z obou stránek
            left_text = left_page.get_text()
            right_text = right_page.get_text()
            
            # Přidání textu jako neviditelné vrstvy pro vyhledávání
            if left_text.strip():
                # Přidání textu z levé stránky
                left_text_dict = left_page.get_text("dict")
                for block in left_text_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                # Přidání textu na správnou pozici
                                text_rect = fitz.Rect(span["bbox"])
                                new_page.insert_text(
                                    (text_rect.x0, text_rect.y0 + text_rect.height),
                                    span["text"],
                                    fontsize=span["size"],
                                    color=(0, 0, 0, 0),  # Průhledný text
                                    overlay=False
                                )
            
            if right_text.strip():
                # Přidání textu z pravé stránky (posunuté doprava)
                right_text_dict = right_page.get_text("dict")
                for block in right_text_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                # Přidání textu na správnou pozici (posunuté doprava)
                                text_rect = fitz.Rect(span["bbox"])
                                new_page.insert_text(
                                    (text_rect.x0 + left_rect.width, text_rect.y0 + text_rect.height),
                                    span["text"],
                                    fontsize=span["size"],
                                    color=(0, 0, 0, 0),  # Průhledný text
                                    overlay=False
                                )
            
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
            
            logger.info(f"PDF s textem úspěšně vytvořeno: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Chyba při vytváření PDF s textem: {e}")
            return False
    
    def create_side_by_side_pdf_simple_text(self, left_pdf: Path, right_pdf: Path, output_path: Path, 
                                           rotation: int = -90, dpi: int = 300) -> bool:
        """
        Vytvoří PDF s jednoduchým přidáním textu pro vyhledávání
        
        Args:
            left_pdf: Cesta k levému PDF (sudé číslo)
            right_pdf: Cesta k pravému PDF (liché číslo)
            output_path: Cesta pro výstupní PDF
            rotation: Úhel rotace (90 nebo -90 stupňů)
            dpi: DPI pro tiskárny (300 je standardní)
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
            
            # Konverze stránek na obrázky s vysokým DPI pro kvalitu
            mat = fitz.Matrix(dpi/72, dpi/72)  # Profesionální DPI (300)
            
            left_pix = left_page.get_pixmap(matrix=mat)
            right_pix = right_page.get_pixmap(matrix=mat)
            
            # Vložení obrázků
            left_img_rect = fitz.Rect(0, 0, left_rect.width, left_rect.height)
            right_img_rect = fitz.Rect(left_rect.width, 0, new_width, right_rect.height)
            
            new_page.insert_image(left_img_rect, pixmap=left_pix)
            new_page.insert_image(right_img_rect, pixmap=right_pix)
            
            # Jednoduché přidání textu pro vyhledávání
            left_text = left_page.get_text()
            right_text = right_page.get_text()
            
            # Přidání textu jako neviditelné vrstvy
            if left_text.strip():
                # Přidání textu z levé stránky na pozici (0,0) s malým fontem
                new_page.insert_text(
                    (10, 10),
                    left_text,
                    fontsize=1,  # Velmi malý font
                    color=(0, 0, 0, 0),  # Průhledný text
                    overlay=False
                )
            
            if right_text.strip():
                # Přidání textu z pravé stránky na pozici (posunuté doprava)
                new_page.insert_text(
                    (left_rect.width + 10, 10),
                    right_text,
                    fontsize=1,  # Velmi malý font
                    color=(0, 0, 0, 0),  # Průhledný text
                    overlay=False
                )
            
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
            
            logger.info(f"PDF s jednoduchým textem úspěšně vytvořeno: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Chyba při vytváření PDF s jednoduchým textem: {e}")
            return False
    
    def merge_pairs(self, rotation: int = -90, mode: str = "simple_text", dpi: int = 300) -> list:
        """
        Spojí páry PDF souborů do dvoustran
        
        Args:
            rotation: Úhel rotace (90 nebo -90 stupňů)
            mode: Režim ("with_text", "simple_text")
            dpi: DPI pro tiskárny (300 je standardní)
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
                    output_name = f"merged_{page_num:02d}_{right_page_num:02d}_{mode}_{dpi}dpi.pdf"
                    output_path = self.output_dir / output_name
                    
                    logger.info(f"Spojuji {left_pdf.name} (levá) a {right_pdf.name} (pravá) - režim: {mode}, DPI: {dpi}")
                    
                    success = False
                    if mode == "with_text":
                        success = self.create_side_by_side_pdf_with_text(left_pdf, right_pdf, output_path, rotation, dpi)
                    elif mode == "simple_text":
                        success = self.create_side_by_side_pdf_simple_text(left_pdf, right_pdf, output_path, rotation, dpi)
                    
                    if success:
                        merged_files.append(output_path)
                    else:
                        logger.error(f"Selhalo spojení páru {page_num}-{right_page_num}")
                else:
                    logger.warning(f"Nenalezena pravá stránka pro stránku {page_num}")
        
        return merged_files


def main():
    """Hlavní funkce aplikace"""
    parser = argparse.ArgumentParser(description="Text Preserving PDF Merger - Spojování PDF souborů s zachováním textu")
    parser.add_argument("--files-dir", default="files", help="Složka s PDF soubory")
    parser.add_argument("--rotation", type=int, default=-90, choices=[90, -90], 
                       help="Úhel rotace (90 nebo -90 stupňů)")
    parser.add_argument("--mode", choices=["with_text", "simple_text"], default="simple_text",
                       help="Režim: with_text (zachování pozic), simple_text (jednoduché přidání)")
    parser.add_argument("--dpi", type=int, default=300, choices=[150, 300, 600],
                       help="DPI pro tiskárny (300 je standardní)")
    parser.add_argument("--auto", action="store_true", help="Automatické spojení všech párových souborů")
    
    args = parser.parse_args()
    
    # Vytvoření instance TextPreservingPDFMerger
    merger = TextPreservingPDFMerger(args.files_dir)
    
    if args.auto:
        # Automatické spojení všech párových souborů
        logger.info(f"Spouštím automatické spojování všech párových souborů - režim: {args.mode}, DPI: {args.dpi}")
        merged_files = merger.merge_pairs(args.rotation, args.mode, args.dpi)
        
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
        print("  python text_preserving_pdf_merger.py --auto --mode simple_text --dpi 300  # S textem pro vyhledávání")
        print("  python text_preserving_pdf_merger.py --auto --mode with_text --dpi 300    # S zachováním pozic textu")


if __name__ == "__main__":
    main()
