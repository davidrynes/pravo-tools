#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test logiky pro oboustranný tisk
"""

print("=" * 90)
print("LOGIKA PRO OBOUSTRANNÝ TISK")
print("=" * 90)

print("""
Pro OBOUSTRANNÝ TISK v tiskárně:

┌─────────────────────────────────────────────────────────────┐
│  PŘEDNÍ STRANA (sudá-lichá):  2-3, 4-5, 6-7                 │
│  → Rotace JEDNÍM SMĚREM (např. +90°)                        │
├─────────────────────────────────────────────────────────────┤
│  ZADNÍ STRANA (lichá-sudá):   3-4, 5-6, 7-8                 │
│  → Rotace OPAČNÝM SMĚREM (např. -90°)                       │
└─────────────────────────────────────────────────────────────┘

PRAVIDLO:
- Pokud LEVÁ stránka je SUDÁ (2, 4, 6...)  → +90° (doprava) ↻
- Pokud LEVÁ stránka je LICHÁ (3, 5, 7...) → -90° (doleva)  ↺
""")

test_pairs = [
    # (left, right, description)
    (2, 3, "Přední strana - sudá vlevo"),
    (4, 5, "Přední strana - sudá vlevo"),
    (6, 7, "Přední strana - sudá vlevo"),
    (3, 4, "Zadní strana - lichá vlevo"),
    (5, 6, "Zadní strana - lichá vlevo"),
    (7, 8, "Zadní strana - lichá vlevo"),
]

print("\n📋 TESTOVACÍ PÁRY:\n")

for left, right, desc in test_pairs:
    left_parity = "sudá" if left % 2 == 0 else "lichá"
    right_parity = "sudá" if right % 2 == 0 else "lichá"
    
    # SPRÁVNÁ LOGIKA PRO OBOUSTRANNÝ TISK:
    # - Levá sudá → +90°
    # - Levá lichá → -90°
    if left % 2 == 0:  # Levá je sudá
        rotation = "+90°"
        symbol = "↻"
    else:  # Levá je lichá
        rotation = "-90°"
        symbol = "↺"
    
    print(f"Pár {left}-{right}: Levá {left} ({left_parity}) + Pravá {right} ({right_parity})")
    print(f"  → {desc}")
    print(f"  → Rotace: {rotation} {symbol}")
    print()

print("=" * 90)
print("ZÁVĚR:")
print("=" * 90)
print("""
Pro oboustranný tisk v tiskárně MUSÍ být logika jednoduchá:

✅ SPRÁVNÁ LOGIKA:
   if left_page % 2 == 0:  # Sudá vlevo
       rotation = +90°
   else:  # Lichá vlevo
       rotation = -90°

To zajistí, že:
  - Všechny přední strany (2-3, 4-5, 6-7) budou otočeny +90° ↻
  - Všechny zadní strany (3-4, 5-6, 7-8) budou otočeny -90° ↺
  - Po složení budou správně orientované!
""")
print("=" * 90)

