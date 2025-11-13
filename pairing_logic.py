#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logika párování pro novinový tisk
Podporuje pevné klíče pro různé rozsahy vydání
"""

from typing import Dict, List, Tuple

# Klíče párování pro různé rozsahy vydání
PAIRING_KEYS = {
    32: [
        (32, 1), (2, 31), (30, 3), (4, 29), (28, 5), (6, 27), (26, 7), (8, 25),
        (24, 9), (10, 23), (22, 11), (12, 21), (20, 13), (14, 19), (18, 15), (16, 17)
    ],
    36: [
        (36, 1), (2, 35), (34, 3), (4, 33), (32, 5), (6, 31), (30, 7), (8, 29),
        (28, 9), (10, 27), (26, 11), (12, 25), (24, 13), (14, 23), (22, 15), (16, 21),
        (20, 17), (18, 19)
    ],
    40: [
        (40, 1), (2, 39), (38, 3), (4, 37), (36, 5), (6, 35), (34, 7), (8, 33),
        (32, 9), (10, 31), (30, 11), (12, 29), (28, 13), (14, 27), (26, 15), (16, 25),
        (24, 17), (18, 23), (22, 19), (20, 21)
    ],
    48: [
        (48, 1), (2, 47), (46, 3), (4, 45), (44, 5), (6, 43), (42, 7), (8, 41),
        (40, 9), (10, 39), (38, 11), (12, 37), (36, 13), (14, 35), (34, 15), (16, 33),
        (32, 17), (18, 31), (30, 19), (20, 29), (28, 21), (22, 27), (26, 23), (24, 25)
    ],
    56: [
        (56, 1), (2, 55), (54, 3), (4, 53), (52, 5), (6, 51), (50, 7), (8, 49),
        (48, 9), (10, 47), (46, 11), (12, 45), (44, 13), (14, 43), (42, 15), (16, 41),
        (40, 17), (18, 39), (38, 19), (20, 37), (36, 21), (22, 35), (34, 23), (24, 33),
        (32, 25), (26, 31), (30, 27), (28, 29)
    ]
}


def get_pairing_key(page_count: int) -> List[Tuple[int, int]]:
    """
    Vrátí klíč párování pro daný počet stran
    
    Args:
        page_count: Počet stran (32, 36, 40, 48, 56)
    
    Returns:
        Seznam párů (levá, pravá) pro oboustranný tisk
        Liché strany jsou vždy vpravo!
    """
    if page_count not in PAIRING_KEYS:
        raise ValueError(f"Nepodporovaný počet stran: {page_count}. Podporované: {list(PAIRING_KEYS.keys())}")
    
    return PAIRING_KEYS[page_count]


def get_pair_for_page(page_number: int, page_count: int) -> Tuple[int, int] | None:
    """
    Vrátí pár pro danou stránku podle klíče
    
    Args:
        page_number: Číslo stránky
        page_count: Celkový počet stran
    
    Returns:
        Pár (levá, pravá) nebo None pokud stránka není v klíči
    """
    pairing_key = get_pairing_key(page_count)
    
    for left, right in pairing_key:
        if left == page_number or right == page_number:
            return (left, right)
    
    return None


def validate_pair(left_page: int, right_page: int, page_count: int) -> bool:
    """
    Zkontroluje zda je pár validní podle klíče
    
    Args:
        left_page: Levá stránka
        right_page: Pravá stránka
        page_count: Celkový počet stran
    
    Returns:
        True pokud je pár validní
    """
    pairing_key = get_pairing_key(page_count)
    
    # Normalizujeme - liché vždy vpravo
    if left_page % 2 == 1:  # Levá je lichá
        left_page, right_page = right_page, left_page
    
    return (left_page, right_page) in pairing_key


def auto_pair_files(files: List[Dict], page_count: int) -> List[Dict]:
    """
    Automaticky spáruje soubory podle klíče
    
    Args:
        files: Seznam souborů s 'filename' a 'page_number'
        page_count: Celkový počet stran
    
    Returns:
        Seznam párů {'left_file', 'right_file', 'left_page', 'right_page'}
    """
    pairing_key = get_pairing_key(page_count)
    
    # Vytvoříme slovník page_number -> filename
    page_to_file = {file['page_number']: file['filename'] for file in files}
    
    pairs = []
    for left_page, right_page in pairing_key:
        # Musíme mít obě stránky
        if left_page in page_to_file and right_page in page_to_file:
            pairs.append({
                'left_file': page_to_file[left_page],
                'right_file': page_to_file[right_page],
                'left_page': left_page,
                'right_page': right_page
            })
    
    return pairs


def ensure_odd_on_right(left_page: int, right_page: int, left_file: str, right_file: str) -> Tuple[int, int, str, str]:
    """
    Zajistí že liché číslo je vždy vpravo
    
    Args:
        left_page: Číslo levé stránky
        right_page: Číslo pravé stránky
        left_file: Název levého souboru
        right_file: Název pravého souboru
    
    Returns:
        Tuple (left_page, right_page, left_file, right_file) s lichým vpravo
    """
    # Pokud je levá stránka lichá, prohodíme
    if left_page % 2 == 1:
        return right_page, left_page, right_file, left_file
    
    return left_page, right_page, left_file, right_file


if __name__ == "__main__":
    # Test
    print("=" * 80)
    print("KLÍČE PÁROVÁNÍ PRO NOVINOVÝ TISK")
    print("=" * 80)
    
    for page_count in [32, 36, 40, 48, 56]:
        print(f"\n📰 {page_count} stran:")
        pairing_key = get_pairing_key(page_count)
        for i, (left, right) in enumerate(pairing_key, 1):
            print(f"  {i:2d}. pár: {left:2d} - {right:2d}  (Liché vpravo: {'✅' if right % 2 == 1 else '❌'})")
    
    print("\n" + "=" * 80)
    print("TEST VALIDACE PÁRU")
    print("=" * 80)
    
    test_cases = [
        (40, 40, 1, True, "Platný pár pro 40 stran"),
        (40, 2, 39, True, "Platný pár pro 40 stran"),
        (40, 2, 3, False, "Neplatný pár (vedlejší strany)"),
        (40, 10, 10, False, "Neplatný pár (stejné strany)"),
    ]
    
    for page_count, left, right, expected, desc in test_cases:
        result = validate_pair(left, right, page_count)
        status = "✅" if result == expected else "❌"
        print(f"{status} {desc}: {left}-{right} → {result}")
    
    print("\n" + "=" * 80)

