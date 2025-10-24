#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Merger - Test script pro ověření funkčnosti
Autor: David Rynes
"""

import sys
from pathlib import Path

# Přidání cesty k modulům
sys.path.insert(0, str(Path(__file__).parent))

from advanced_pdf_merger import AdvancedPDFMerger

def test_pdf_merger():
    """Test základní funkčnosti PDF merger"""
    print("=== PDF Merger - Test funkčnosti ===")
    print()
    
    # Vytvoření instance
    merger = AdvancedPDFMerger()
    
    # Kontrola existence souborů
    pdf_files = merger.get_pdf_files()
    print(f"Nalezeno {len(pdf_files)} PDF souborů:")
    for i, pdf_file in enumerate(pdf_files, 1):
        page_num = merger.parse_page_number(pdf_file.name)
        print(f"  {i:2d}. {pdf_file.name} (číslo stránky: {page_num})")
    
    print()
    
    # Test automatického párování
    if len(pdf_files) >= 2:
        print("Test automatického párování...")
        merged_files = merger.merge_pairs()
        
        if merged_files:
            print(f"✅ Úspěšně vytvořeno {len(merged_files)} spojených PDF souborů:")
            for file in merged_files:
                print(f"  - {file}")
        else:
            print("❌ Nebyl vytvořen žádný spojený PDF soubor")
    else:
        print("❌ Potřebujete alespoň 2 PDF soubory pro test")
    
    print()
    print("Test dokončen!")

if __name__ == "__main__":
    test_pdf_merger()
