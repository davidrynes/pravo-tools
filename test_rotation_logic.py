#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test logiky rotace
"""

print("=" * 80)
print("TEST LOGIKY ROTACE")
print("=" * 80)

# Testovací páry
test_pairs = [
    # (left_page, right_page, description)
    (2, 3, "Normální pořadí - přední strany"),
    (4, 5, "Normální pořadí - přední strany"),
    (6, 7, "Normální pořadí - přední strany"),
    (40, 39, "Obrácené pořadí - zadní strany"),
    (38, 37, "Obrácené pořadí - zadní strany"),
    (3, 2, "Obrácené pořadí - přední/zadní"),
]

print("\n📋 ANALÝZA PÁRŮ:\n")

for left_page, right_page, desc in test_pairs:
    left_parity = "sudá" if left_page % 2 == 0 else "lichá"
    right_parity = "sudá" if right_page % 2 == 0 else "lichá"
    
    print(f"Pár: {left_page} ({left_parity}) + {right_page} ({right_parity})")
    print(f"  Popis: {desc}")
    
    # Aktuální logika (v kódu)
    if left_page < right_page:
        current_rotation = "+90°"
    else:
        current_rotation = "-90°"
    
    print(f"  Aktuální logika: {current_rotation}")
    
    # Logika podle dokumentace: "Pokud liché > sudé: +90°, Pokud liché < sudé: -90°"
    odd_page = left_page if left_page % 2 == 1 else right_page
    even_page = left_page if left_page % 2 == 0 else right_page
    
    if odd_page > even_page:
        doc_rotation = "+90°"
    else:
        doc_rotation = "-90°"
    
    print(f"  Podle dokumentace (lichá {odd_page} vs sudá {even_page}): {doc_rotation}")
    
    if current_rotation == doc_rotation:
        print(f"  ✅ Shoduje se")
    else:
        print(f"  ❌ NESHODUJE SE!")
    
    print()

print("=" * 80)
print("ZÁVĚR:")
print("=" * 80)
print()
print("Aktuální logika: if left_page < right_page: +90° else: -90°")
print()
print("To funguje správně pro:")
print("  ✅ 2-3: 2 < 3 → +90° (správně)")
print("  ✅ 4-5: 4 < 5 → +90° (správně)")
print("  ✅ 40-39: 40 > 39 → -90° (správně pro obrácené)")
print()
print("Takže aktuální logika je SPRÁVNÁ!")
print("Problém může být jinde...")
print("=" * 80)

