#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pro ověření PDF/X-1a:2001 metadat
"""

import fitz
from pathlib import Path

def check_pdf_metadata(pdf_path):
    """Zkontroluje metadata PDF souboru"""
    print("=" * 80)
    print(f"KONTROLA METADAT: {pdf_path.name}")
    print("=" * 80)
    
    try:
        doc = fitz.open(str(pdf_path))
        
        # Získání metadat
        metadata = doc.metadata
        
        print("\n📋 METADATA:")
        for key, value in metadata.items():
            if value:
                print(f"  {key:15s}: {value}")
        
        # Kontrola PDF/X profilu
        print("\n🔍 KONTROLA PDF/X-1a:2001:")
        
        has_format = 'format' in metadata and metadata['format']
        has_pdfx = has_format and 'PDF/X' in metadata['format']
        
        if has_pdfx:
            print(f"  ✅ PDF/X profil nalezen: {metadata['format']}")
        else:
            print(f"  ❌ PDF/X profil nenalezen")
            if has_format:
                print(f"     Nalezený formát: {metadata['format']}")
            else:
                print(f"     Formát není specifikován")
        
        # Další důležité informace
        print(f"\n📊 DALŠÍ INFORMACE:")
        print(f"  Počet stránek: {doc.page_count}")
        print(f"  Velikost: {pdf_path.stat().st_size / (1024 * 1024):.2f} MB")
        
        # První stránka
        if doc.page_count > 0:
            page = doc[0]
            print(f"  Rozměry: {page.rect.width:.0f} x {page.rect.height:.0f} px")
            print(f"  Rotace: {page.rotation}°")
        
        doc.close()
        
        print("\n" + "=" * 80)
        return has_pdfx
        
    except Exception as e:
        print(f"❌ Chyba při kontrole: {e}")
        return False


if __name__ == "__main__":
    print("🧪 TEST PDF/X-1a:2001 METADAT\n")
    
    # Hledáme merged PDF soubory
    output_dir = Path("output")
    
    if not output_dir.exists():
        print("❌ Složka 'output' neexistuje")
        exit(1)
    
    merged_files = list(output_dir.glob("merged_*_web.pdf"))
    
    if not merged_files:
        print("❌ Žádné merged PDF soubory nenalezeny v 'output' složce")
        print("   Spusťte nejprve merge operaci v aplikaci")
        exit(1)
    
    print(f"📁 Nalezeno {len(merged_files)} merged PDF souborů:\n")
    
    results = []
    for pdf_file in merged_files:
        has_pdfx = check_pdf_metadata(pdf_file)
        results.append((pdf_file.name, has_pdfx))
        print()
    
    # Souhrn
    print("=" * 80)
    print("📊 SOUHRN:")
    print("=" * 80)
    
    success_count = sum(1 for _, has_pdfx in results if has_pdfx)
    total_count = len(results)
    
    for filename, has_pdfx in results:
        status = "✅" if has_pdfx else "❌"
        print(f"  {status} {filename}")
    
    print(f"\n  Úspěšných: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n✅ VŠECHNY PDF SOUBORY MAJÍ PDF/X-1a:2001 PROFIL!")
    else:
        print(f"\n⚠️  {total_count - success_count} souborů nemá PDF/X profil")
    
    print("=" * 80)

