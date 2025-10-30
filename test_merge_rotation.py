#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test merge s rotací - simulace reálného použití
"""

from pathlib import Path

# Simulace funkce parse_page_number
def parse_page_number(filename: str) -> int:
    name = Path(filename).stem
    if len(name) >= 5:
        page_chars = name[-5:-3]
        if page_chars.isdigit():
            return int(page_chars)
    return 0

# Testovací páry
test_pairs = [
    {'left_file': 'PR25103002VY1.pdf', 'right_file': 'PR25103003VY1.pdf'},
    {'left_file': 'PR25103004VY1.pdf', 'right_file': 'PR25103005VY1.pdf'},
    {'left_file': 'PR25103040VY1.pdf', 'right_file': 'PR25103039VY1.pdf'},
]

print("=" * 80)
print("TEST MERGE S ROTACÍ - SIMULACE")
print("=" * 80)

for i, pair in enumerate(test_pairs, 1):
    print(f"\n{i}. Pár:")
    
    left_file = pair['left_file']
    right_file = pair['right_file']
    
    left_page = parse_page_number(left_file)
    right_page = parse_page_number(right_file)
    
    left_parity = "sudá" if left_page % 2 == 0 else "lichá"
    right_parity = "sudá" if right_page % 2 == 0 else "lichá"
    
    print(f"  Levý:  {left_file} → Strana {left_page:2d} ({left_parity})")
    print(f"  Pravý: {right_file} → Strana {right_page:2d} ({right_parity})")
    
    # Dynamická rotace podle pořadí stránek (aktuální logika)
    if left_page < right_page:
        rotation = 90
        desc = "rostoucí pořadí"
    else:
        rotation = -90
        desc = "klesající pořadí"
    
    print(f"  → Rotace: {rotation:+3d}° ({desc})")
    print(f"  → Výstup: merged_{left_page:02d}_{right_page:02d}_web.pdf")

print("\n" + "=" * 80)

