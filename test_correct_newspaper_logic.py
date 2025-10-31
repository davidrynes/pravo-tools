#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test SPRÁVNÉ logiky pro oboustranný tisk dvojstran
"""

print("=" * 90)
print("OBOUSTRANNÝ TISK DVOJSTRAN - SPRÁVNÁ LOGIKA")
print("=" * 90)

print("""
OBOUSTRANNÝ TISK DVOJSTRAN:

┌─────────────────────────────────────────────────────────────────┐
│                    FYZICKÝ PAPÍR 1                              │
├─────────────────────────────────────────────────────────────────┤
│  PŘEDNÍ: 1. pár (2-3) → Rotace +90° ↻                         │
│  ZADNÍ:  2. pár (4-5) → Rotace -90° ↺                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    FYZICKÝ PAPÍR 2                              │
├─────────────────────────────────────────────────────────────────┤
│  PŘEDNÍ: 3. pár (6-7) → Rotace +90° ↻                         │
│  ZADNÍ:  4. pár (8-9) → Rotace -90° ↺                         │
└─────────────────────────────────────────────────────────────────┘

LOGIKA:
- Páry s LICHÝM pořadím (1., 3., 5. pár) = PŘEDNÍ → +90°
- Páry se SUDÝM pořadím (2., 4., 6. pár) = ZADNÍ  → -90°
""")

test_pairs = [
    # (left, right, pair_index, očekávaná_rotace)
    (2, 3, 1, +90, "1. pár - Přední strana papíru 1"),
    (4, 5, 2, -90, "2. pár - Zadní strana papíru 1"),
    (6, 7, 3, +90, "3. pár - Přední strana papíru 2"),
    (8, 9, 4, -90, "4. pár - Zadní strana papíru 2"),
    (10, 11, 5, +90, "5. pár - Přední strana papíru 3"),
    (12, 13, 6, -90, "6. pár - Zadní strana papíru 3"),
]

print("\n📋 TESTOVACÍ PÁRY:\n")

all_passed = True

for left, right, pair_index, expected, desc in test_pairs:
    # SPRÁVNÁ LOGIKA PRO OBOUSTRANNÝ TISK DVOJSTRAN:
    # - Liché pořadí páru (1, 3, 5...) = Přední → +90°
    # - Sudé pořadí páru (2, 4, 6...) = Zadní → -90°
    
    if pair_index % 2 == 1:  # Liché pořadí = Přední
        rotation = +90
        side = "Přední"
    else:  # Sudé pořadí = Zadní
        rotation = -90
        side = "Zadní"
    
    status = "✅" if rotation == expected else "❌"
    if rotation != expected:
        all_passed = False
    
    print(f"{status} Pár {left}-{right} ({pair_index}. pár): {desc}")
    print(f"   {side} strana papíru → Rotace: {rotation:+3d}° (očekáváno: {expected:+3d}°)")
    print()

print("=" * 90)
if all_passed:
    print("✅ VŠECHNY TESTY PROŠLY!")
else:
    print("❌ NĚKTERÉ TESTY SELHALY!")
print("=" * 90)

print("\n💡 IMPLEMENTACE:\n")
print("""
V kódu potřebujeme sledovat POŘADÍ PÁRU (index v listu párů):

for i, pair in enumerate(file_pairs, start=1):  # start=1 pro 1-based index
    left_page = pair['left_page']
    right_page = pair['right_page']
    
    # Rotace podle pořadí páru
    if i % 2 == 1:  # Liché pořadí (1, 3, 5...) = Přední
        rotation = +90
    else:           # Sudé pořadí (2, 4, 6...) = Zadní
        rotation = -90
""")

print("\n🖨️ PROCES V TISKÁRNĚ:\n")
print("""
PAPÍR 1:
  Tisk přední: Pár 2-3 (rotace +90°)
  Otočení papíru
  Tisk zadní:  Pár 4-5 (rotace -90°)
  → Po složení správně orientováno ✅

PAPÍR 2:
  Tisk přední: Pár 6-7 (rotace +90°)
  Otočení papíru
  Tisk zadní:  Pár 8-9 (rotace -90°)
  → Po složení správně orientováno ✅
""")

print("=" * 90)

