#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finální test rotace pro oboustranný tisk
"""

print("=" * 90)
print("FINÁLNÍ TEST ROTACE PRO OBOUSTRANNÝ TISK")
print("=" * 90)

test_pairs = [
    # (left, right, očekávaná_rotace, typ)
    (2, 3, +90, "Přední strana"),
    (3, 4, -90, "Zadní strana"),
    (4, 5, +90, "Přední strana"),
    (5, 6, -90, "Zadní strana"),
    (6, 7, +90, "Přední strana"),
    (7, 8, -90, "Zadní strana"),
]

print("\n📋 VŠECHNY TESTOVACÍ PÁRY:\n")

all_passed = True

for left, right, expected, typ in test_pairs:
    # FINÁLNÍ SPRÁVNÁ LOGIKA
    if left % 2 == 0:  # Levá je sudá
        rotation = +90
    else:  # Levá je lichá
        rotation = -90
    
    status = "✅" if rotation == expected else "❌"
    if rotation != expected:
        all_passed = False
    
    print(f"{status} Pár {left}-{right}: {typ}")
    print(f"   Rotace: {rotation:+3d}° (očekáváno: {expected:+3d}°)")
    print()

print("=" * 90)
if all_passed:
    print("✅ VŠECHNY TESTY PROŠLY!")
else:
    print("❌ NĚKTERÉ TESTY SELHALY!")
print("=" * 90)

print("\n🖨️ VIZUALIZACE OBOUSTRANNÉHO TISKU:\n")
print("""
┌─────────────────────────────────────────────────────────────────┐
│                      OBOUSTRANNÝ TISK                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LIST 1:                                                        │
│    Přední strana: 2-3  → Rotace +90° ↻                        │
│    Zadní strana:  3-4  → Rotace -90° ↺                        │
│                                                                 │
│  LIST 2:                                                        │
│    Přední strana: 4-5  → Rotace +90° ↻                        │
│    Zadní strana:  5-6  → Rotace -90° ↺                        │
│                                                                 │
│  LIST 3:                                                        │
│    Přední strana: 6-7  → Rotace +90° ↻                        │
│    Zadní strana:  7-8  → Rotace -90° ↺                        │
│                                                                 │
│  → Po složení budou všechny strany správně orientované! ✅     │
└─────────────────────────────────────────────────────────────────┘
""")

print("\n📐 PRAVIDLO:\n")
print("  if left_page % 2 == 0:  # Levá je sudá")
print("      rotation = +90°     # Přední strana")
print("  else:                    # Levá je lichá")
print("      rotation = -90°     # Zadní strana")
print()
print("=" * 90)

