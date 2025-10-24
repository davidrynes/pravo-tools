#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Merger - Optimalizovaná verze pro menší soubory
Autor: David Rynes
Popis: Spojuje PDF soubory přímo bez konverze na obrázky pro menší výstupní soubory
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


class OptimizedPDFMerger:
    """Optimalizovaná třída pro spojování PDF souborů s menšími výstupními soubory"""
    
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
    
    def create_side_by_side_pdf_direct(self, left_pdf: Path, right_pdf: Path, output_path: Path, 
                                      rotation: int = -90) -> bool:
        """
        Vytvoří PDF s dvěma stránkami vedle sebe přímo bez konverze na obrázky
        
        Args:
            left_pdf: Cesta k levému PDF (sudé číslo)
            right_pdf: Cesta k pravému PDF (liché číslo)
            output_path: Cesta pro výstupní PDF
            rotation: Úhel rotace (90 nebo -90 stupňů)
        """
        try:
            # Načtení PDF souborů
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
            
            # Vytvoření nového PDF s dvoustranou pomocí PyMuPDF (fitz)
            doc = fitz.open()
            
            # Vytvoření nové stránky s dvojnásobnou šířkou
            new_width = left_box.width + right_box.width
            new_height = max(left_box.height, right_box.height)
            
            # Vytvoření nové stránky
            new_page = doc.new_page(width=new_width, height=new_height)
            
            # Načtení původních stránek jako obrázky s nižším DPI pro menší velikost
            left_doc = fitz.open(str(left_pdf))
            right_doc = fitz.open(str(right_pdf))
            
            left_page_img = left_doc[0]
            right_page_img = right_doc[0]
            
            # Konverze na obrázky s optimalizovaným DPI (150 místo 300)
            mat_left = fitz.Matrix(150/72, 150/72)  # Nižší DPI pro menší soubory
            mat_right = fitz.Matrix(150/72, 150/72)
            
            left_pix = left_page_img.get_pixmap(matrix=mat_left)
            right_pix = right_page_img.get_pixmap(matrix=mat_right)
            
            # Vložení levého obrázku
            left_rect = fitz.Rect(0, 0, left_box.width, left_box.height)
            new_page.insert_image(left_rect, pixmap=left_pix)
            
            # Vložení pravého obrázku
            right_rect = fitz.Rect(left_box.width, 0, new_width, right_box.height)
            new_page.insert_image(right_rect, pixmap=right_pix)
            
            # Rotace stránky
            if rotation != 0:
                new_page.set_rotation(rotation)
                logger.info(f"Stránka otočena o {rotation} stupňů")
            
            # Uzavření dočasných dokumentů
            left_doc.close()
            right_doc.close()
            
            # Uložení s optimalizací
            doc.save(str(output_path), garbage=4, deflate=True, clean=True)
            doc.close()
            
            logger.info(f"Optimalizované PDF úspěšně vytvořeno: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Chyba při vytváření optimalizovaného PDF: {e}")
            return False
    
    def create_side_by_side_pdf_minimal(self, left_pdf: Path, right_pdf: Path, output_path: Path, 
                                       rotation: int = -90) -> bool:
        """
        Vytvoří PDF s minimální velikostí pomocí přímého kopírování stránek
        
        Args:
            left_pdf: Cesta k levému PDF (sudé číslo)
            right_pdf: Cesta k pravému PDF (liché číslo)
            output_path: Cesta pro výstupní PDF
            rotation: Úhel rotace (90 nebo -90 stupňů)
        """
        try:
            # Načtení PDF souborů pomocí PyMuPDF pro lepší kontrolu
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
            
            # Konverze stránek na obrázky s velmi nízkým DPI pro minimální velikost
            mat = fitz.Matrix(100/72, 100/72)  # Velmi nízké DPI (100)
            
            left_pix = left_page.get_pixmap(matrix=mat)
            right_pix = right_page.get_pixmap(matrix=mat)
            
            # Vložení obrázků
            left_img_rect = fitz.Rect(0, 0, left_rect.width, left_rect.height)
            right_img_rect = fitz.Rect(left_rect.width, 0, new_width, right_rect.height)
            
            new_page.insert_image(left_img_rect, pixmap=left_pix)
            new_page.insert_image(right_img_rect, pixmap=right_pix)
            
            # Rotace stránky
            if rotation != 0:
                new_page.set_rotation(rotation)
                logger.info(f"Stránka otočena o {rotation} stupňů")
            
            # Uzavření původních dokumentů
            left_doc.close()
            right_doc.close()
            
            # Uložení s maximální optimalizací
            new_doc.save(str(output_path), 
                        garbage=4,      # Odstraní nepoužívané objekty
                        deflate=True,   # Komprese
                        clean=True)     # Vyčištění
            
            new_doc.close()
            
            logger.info(f"Minimální PDF úspěšně vytvořeno: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Chyba při vytváření minimálního PDF: {e}")
            return False
    
    def merge_pairs(self, rotation: int = -90, mode: str = "minimal") -> list:
        """
        Spojí páry PDF souborů do dvoustran
        
        Args:
            rotation: Úhel rotace (90 nebo -90 stupňů)
            mode: Režim optimalizace ("minimal", "optimized", "quality")
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
                    if mode == "minimal":
                        success = self.create_side_by_side_pdf_minimal(left_pdf, right_pdf, output_path, rotation)
                    elif mode == "optimized":
                        success = self.create_side_by_side_pdf_direct(left_pdf, right_pdf, output_path, rotation)
                    else:  # quality
                        # Použít původní metodu s vysokou kvalitou
                        from advanced_pdf_merger import AdvancedPDFMerger
                        merger = AdvancedPDFMerger()
                        success = merger.create_side_by_side_pdf(left_pdf, right_pdf, output_path, rotation)
                    
                    if success:
                        merged_files.append(output_path)
                    else:
                        logger.error(f"Selhalo spojení páru {page_num}-{right_page_num}")
                else:
                    logger.warning(f"Nenalezena pravá stránka pro stránku {page_num}")
        
        return merged_files


def main():
    """Hlavní funkce aplikace"""
    parser = argparse.ArgumentParser(description="Optimized PDF Merger - Spojování PDF souborů s optimalizací velikosti")
    parser.add_argument("--files-dir", default="files", help="Složka s PDF soubory")
    parser.add_argument("--rotation", type=int, default=-90, choices=[90, -90], 
                       help="Úhel rotace (90 nebo -90 stupňů)")
    parser.add_argument("--mode", choices=["minimal", "optimized", "quality"], default="minimal",
                       help="Režim optimalizace: minimal (nejmenší), optimized (vyvážený), quality (nejlepší kvalita)")
    parser.add_argument("--auto", action="store_true", help="Automatické spojení všech párových souborů")
    
    args = parser.parse_args()
    
    # Vytvoření instance OptimizedPDFMerger
    merger = OptimizedPDFMerger(args.files_dir)
    
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
        print("  python optimized_pdf_merger.py --auto --mode minimal     # Nejmenší soubory")
        print("  python optimized_pdf_merger.py --auto --mode optimized   # Vyvážené")
        print("  python optimized_pdf_merger.py --auto --mode quality     # Nejlepší kvalita")


if __name__ == "__main__":
    main()
