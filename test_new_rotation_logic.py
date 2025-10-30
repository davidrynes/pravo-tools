#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test nové logiky rotace - založené na porovnání lichá vs sudá
"""

from pathlib import Path

def parse_page_number(filename: str) -> int:
    name = Path(filename).stem
    if len(name) >= 5:
        page_chars = name[-5:-3]
        if page_chars.isdigit():
            return int(page_chars)
    return 0

# Testovací páry
test_cases = [
    # (left_file, right_file, očekávaná_rotace, popis)
    ('PR25103002VY1.pdf', 'PR25103003VY1.pdf', +90, 'Přední strany - normální pořadí'),
    ('PR25103004VY1.pdf', 'PR25103005VY1.pdf', +90, 'Přední strany - normální pořadí'),
    ('PR25103040VY1.pdf', 'PR25103039VY1.pdf', -90, 'Zadní strany - obrácené pořadí'),
    ('PR25103038VY1.pdf', 'PR25103037VY1.pdf', -90, 'Zadní strany - obrácené pořadí'),
    ('PR25103001VY1.pdf', 'PR25103002VY1.pdf', -90, 'Liché vlevo, sudé vpravo'),
    ('PR25103003VY1.pdf', 'PR25103002VY1.pdf', +90, 'Lichá větší než sudá'),
]

print("=" * 90)
print("TEST NOVÉ LOGIKY ROTACE - ZALOŽENÉ NA POROVNÁNÍ LICHÁ VS SUDÁ")
print("=" * 90)

for left_file, right_file, expected_rotation, desc in test_cases:
    print(f"\nTest: {desc}")
    
    left_page = parse_page_number(left_file)
    right_page = parse_page_number(right_file)
    
    left_parity = "sudá" if left_page % 2 == 0 else "lichá"
    right_parity = "sudá" if right_page % 2 == 0 else "lichá"
    
    print(f"  Levý:  {left_file} → Strana {left_page:2d} ({left_parity})")
    print(f"  Pravý: {right_file} → Strana {right_page:2d} ({right_parity})")
    
    # NOVÁ LOGIKA: založená na porovnání lichá vs sudá
    if left_page % 2 == 0:  # Levá je sudá
        odd_page = right_page
        even_page = left_page
    else:  # Levá je lichá
        odd_page = left_page
        even_page = right_page
    
    # Logika: Pokud liché > sudé: +90°, Pokud liché < sudé: -90°
    if odd_page > even_page:
        rotation = 90
        reason = f"lichá {odd_page} > sudá {even_page}"
    else:
        rotation = -90
        reason = f"lichá {odd_page} < sudá {even_page}"
    
    print(f"  → Lichá: {odd_page}, Sudá: {even_page}")
    print(f"  → Rotace: {rotation:+3d}° ({reason})")
    print(f"  → Očekáváno: {expected_rotation:+3d}°")
    
    if rotation == expected_rotation:
        print(f"  ✅ SPRÁVNĚ")
    else:
        print(f"  ❌ CHYBA! Očekáváno {expected_rotation:+3d}°, ale dostáno {rotation:+3d}°")

print("\n" + "=" * 90)
print("SHRNUTÍ LOGIKY:")
print("=" * 90)
print("""
NOVÁ LOGIKA:
1. Zjistíme, která stránka je lichá a která sudá
2. Porovnáme: lichá vs sudá
3. Pokud lichá > sudá: +90° (doprava)
4. Pokud lichá < sudá: -90° (doleva)

PŘÍKLADY:
- Pár 2-3: lichá (3) > sudá (2) → +90° ✅
- Pár 4-5: lichá (5) > sudá (4) → +90° ✅
- Pár 40-39: lichá (39) < sudá (40) → -90° ✅
- Pár 1-2: lichá (1) < sudá (2) → -90° ✅
- Pár 3-2: lichá (3) > sudá (2) → +90° ✅
""")
print("=" * 90)

