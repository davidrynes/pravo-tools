#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test skript pro ověření parsování reálných souborů
"""

from pathlib import Path
import sys

# Import funkce z web_app
sys.path.insert(0, str(Path(__file__).parent))
from web_app import WebPDFMerger

# Vytvoření instance
merger = WebPDFMerger()

# Cesta k testovacím souborům
files_dir = Path(__file__).parent / "files"

print("=" * 70)
print("TEST PARSOVÁNÍ REÁLNÝCH SOUBORŮ")
print("=" * 70)

# Seznam všech PDF souborů
pdf_files = sorted(files_dir.glob("*.pdf"))

if not pdf_files:
    print("❌ Žádné PDF soubory nenalezeny v složce 'files'")
    sys.exit(1)

print(f"\nNalezeno {len(pdf_files)} PDF souborů:\n")

# Parsování každého souboru
file_data = []
for pdf_file in pdf_files:
    page_num = merger.parse_page_number(pdf_file.name)
    parity = "sudá" if page_num % 2 == 0 else "lichá"
    file_data.append({
        'name': pdf_file.name,
        'page': page_num,
        'parity': parity
    })
    print(f"  📄 {pdf_file.name:45s} → strana {page_num:2d} ({parity})")

# Seskupení podle parity
even_pages = [f for f in file_data if f['page'] % 2 == 0 and f['page'] > 0]
odd_pages = [f for f in file_data if f['page'] % 2 == 1]

print("\n" + "=" * 70)
print("ANALÝZA STRÁNEK")
print("=" * 70)
print(f"\n✅ Sudé stránky (levá strana): {len(even_pages)}")
for f in sorted(even_pages, key=lambda x: x['page']):
    print(f"   - Strana {f['page']:2d}: {f['name']}")

print(f"\n✅ Liché stránky (pravá strana): {len(odd_pages)}")
for f in sorted(odd_pages, key=lambda x: x['page']):
    print(f"   - Strana {f['page']:2d}: {f['name']}")

# Automatické párování
print("\n" + "=" * 70)
print("AUTOMATICKÉ PÁROVÁNÍ")
print("=" * 70)

page_dict = {f['page']: f for f in file_data}
pairs = []

for f in even_pages:
    even_page = f['page']
    odd_page = even_page + 1
    
    if odd_page in page_dict:
        pairs.append({
            'left': even_page,
            'right': odd_page,
            'left_file': f['name'],
            'right_file': page_dict[odd_page]['name']
        })

if pairs:
    print(f"\n✅ Nalezeno {len(pairs)} párů:\n")
    for i, pair in enumerate(pairs, 1):
        print(f"{i}. Pár:")
        print(f"   Levá  (strana {pair['left']:2d}): {pair['left_file']}")
        print(f"   Pravá (strana {pair['right']:2d}): {pair['right_file']}")
        
        # Rotace
        if pair['left'] < pair['right']:
            rotation = "+90°"
            desc = "Standardní pořadí"
        else:
            rotation = "-90°"
            desc = "Obrácené pořadí"
        print(f"   → Rotace: {rotation} ({desc})\n")
else:
    print("\n❌ Žádné páry nebyly nalezeny")

print("=" * 70)

