#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test logiky pro NOVINOVÝ TISK
"""

print("=" * 90)
print("LOGIKA PRO NOVINOVÝ TISK")
print("=" * 90)

print("""
NOVINOVÝ TISK (tradiční):

┌─────────────────────────────────────────────────────────────────┐
│  Každá stránka se používá POUZE JEDNOU!                         │
│                                                                 │
│  TISKOVÝ LIST 1: PDF(2) + PDF(3) = Dvoustrana                  │
│  TISKOVÝ LIST 2: PDF(4) + PDF(5) = Dvoustrana                  │
│  TISKOVÝ LIST 3: PDF(6) + PDF(7) = Dvoustrana                  │
│                                                                 │
│  Tiskárna tiskne DVOUSTRANA najednou (2 strany vedle sebe)     │
│                                                                 │
│  → VŠECHNY LISTY musí být otočeny STEJNÝM SMĚREM!              │
└─────────────────────────────────────────────────────────────────┘

SPRÁVNÁ LOGIKA:
  - VŠECHNY páry (2-3, 4-5, 6-7...) → STEJNÁ rotace (např. -90°)
  - Tiskárna tiskne dvoustrana → Po otočení správně orientováno
""")

test_pairs = [
    (2, 3, "Tiskový list 1"),
    (4, 5, "Tiskový list 2"),
    (6, 7, "Tiskový list 3"),
    (8, 9, "Tiskový list 4"),
]

print("\n📋 TESTOVACÍ PÁRY (NOVINOVÝ TISK):\n")

# Pro novinový tisk: VŠECHNY páry mají STEJNOU rotaci
rotation = -90  # nebo +90, ale všechny STEJNĚ

for left, right, desc in test_pairs:
    left_parity = "sudá" if left % 2 == 0 else "lichá"
    right_parity = "sudá" if right % 2 == 0 else "lichá"
    
    print(f"{desc}:")
    print(f"  PDF {left} ({left_parity}) + PDF {right} ({right_parity})")
    print(f"  → Rotace: {rotation}° (STEJNÁ pro všechny)")
    print(f"  → Používá každou stránku POUZE JEDNOU")
    print()

print("=" * 90)
print("ZÁVĚR:")
print("=" * 90)
print("""
Pro NOVINOVÝ TISK musí být logika NEJJEDNODUŠŠÍ:

✅ SPRÁVNÁ LOGIKA:
   rotation = -90°  # VŠECHNY páry stejně (nebo +90°)
   
   # NEBO pokud chcete volitelnou rotaci:
   rotation = user_selected_rotation  # -90 nebo +90

NENÍ POTŘEBA ŽÁDNÁ PODMÍNKA!
- Všechny páry (2-3, 4-5, 6-7) jsou samostatné tiskové listy
- Každá strana se používá POUZE JEDNOU
- Všechny musí být otočeny STEJNÝM směrem
- Tiskárna je vytiskne jako dvoustrana

To je ZCELA ODLIŠNÉ od klasického oboustranného tisku!
""")
print("=" * 90)

print("\n🖨️ ROZDÍL:\n")
print("""
KLASICKÝ OBOUSTRANNÝ TISK (NÁŠ MINULÝ POKUS):
  List 1 přední: 2-3 (+90°)
  List 1 zadní:  3-4 (-90°)  ← Strana 3 použita 2x! ❌

NOVINOVÝ TISK (SPRÁVNĚ):
  Tiskový list 1: 2-3 (-90°)
  Tiskový list 2: 4-5 (-90°)  ← Každá strana 1x! ✅
  Tiskový list 3: 6-7 (-90°)
  
  Všechny otočeny STEJNĚ!
""")
print("=" * 90)

