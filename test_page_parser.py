#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test skript pro ověření parsování čísel stránek z názvů souborů
"""

from pathlib import Path

def parse_page_number(filename: str) -> int:
    """
    Extrahuje číslo stránky z názvu souboru.
    
    Podporuje formáty:
    1. PRYYMMDDXXBBB.pdf - extrahuje poslední 2 číslice (XX)
    2. název_číslo.pdf - extrahuje číslo za poslední podtržítkem
    
    Příklady:
    - PRAVO_NEW_TEST03_FINAL_02.pdf -> 02
    - PR2501301001.pdf -> 10
    - myfile_15.pdf -> 15
    """
    try:
        name = Path(filename).stem
        
        # Zkusíme extrahovat poslední 2 znaky jako číslo stránky
        if len(name) >= 2:
            last_two = name[-2:]
            if last_two.isdigit():
                return int(last_two)
        
        # Fallback: zkusíme najít číslo za posledním podtržítkem
        parts = name.split('_')
        if parts:
            last_part = parts[-1]
            if last_part.isdigit():
                return int(last_part)
        
        return 0
    except Exception as e:
        print(f"Chyba při parsování čísla stránky z '{filename}': {e}")
        return 0

# Testovací případy
test_files = [
    "PRAVO_NEW_TEST03_FINAL_02.pdf",
    "PRAVO_NEW_TEST03_FINAL_03.pdf",
    "PRAVO_NEW_TEST03_FINAL_14.pdf",
    "PRAVO_NEW_TEST03_FINAL_15.pdf",
    "PRAVO_NEW_TEST03_FINAL_40.pdf",
    "PRAVO_NEW_TEST03_FINAL_39.pdf",
    "PRAVO_NEW_TEST03_FINAL_38.pdf",
    "PRAVO_NEW_TEST03_FINAL_01.pdf",
    "PR2501301001.pdf",
    "PR2501301040.pdf",
    "test_15.pdf",
    "document_05.pdf"
]

print("=" * 60)
print("TEST PARSOVÁNÍ ČÍSEL STRÁNEK Z NÁZVŮ SOUBORŮ")
print("=" * 60)

for filename in test_files:
    page_num = parse_page_number(filename)
    parity = "sudá" if page_num % 2 == 0 else "lichá"
    print(f"{filename:40s} -> strana {page_num:2d} ({parity})")

print("\n" + "=" * 60)
print("TESTOVÁNÍ PÁROVÁNÍ")
print("=" * 60)

# Simulace párování
pages = {}
for filename in test_files:
    page_num = parse_page_number(filename)
    if page_num > 0:
        pages[page_num] = filename

# Vytvoření párů (sudá vlevo, lichá vpravo)
pairs = []
for page_num in sorted(pages.keys()):
    if page_num % 2 == 0:  # Sudá stránka (levá)
        right_page = page_num + 1
        if right_page in pages:
            pairs.append({
                'left': page_num,
                'right': right_page,
                'left_file': pages[page_num],
                'right_file': pages[right_page]
            })

print(f"\nNalezeno {len(pairs)} párů:")
for i, pair in enumerate(pairs, 1):
    print(f"\n{i}. Pár:")
    print(f"   Levá  (strana {pair['left']:2d}): {pair['left_file']}")
    print(f"   Pravá (strana {pair['right']:2d}): {pair['right_file']}")
    
    # Určení rotace
    if pair['left'] < pair['right']:
        rotation = "+90°"
    else:
        rotation = "-90°"
    print(f"   → Rotace: {rotation}")

print("\n" + "=" * 60)

