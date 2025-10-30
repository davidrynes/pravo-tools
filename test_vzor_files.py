#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test skript pro ověření parsování reálných souborů z pdf-vzor
"""

from pathlib import Path

def parse_page_number(filename: str) -> int:
    """
    Extrahuje číslo stránky z názvu souboru.
    
    Podporuje formáty:
    1. PRYYMMDDXXBBB.pdf - XX je na pozici -5:-3 (4. a 5. znak od konce)
    2. název_číslo.pdf - extrahuje číslo za poslední podtržítkem
    
    Příklady:
    - PR25103001VY1.pdf -> 01 (znaky na pozici -5:-3)
    - PR25103040VY1.pdf -> 40 (znaky na pozici -5:-3)
    """
    try:
        name = Path(filename).stem
        
        # Primární metoda: extrahujeme 4. a 5. znak od konce (před posledními 3 znaky)
        # Formát: PRYYMMDDXXBBB -> XX jsou na pozici [-5:-3]
        if len(name) >= 5:
            page_chars = name[-5:-3]
            if page_chars.isdigit():
                return int(page_chars)
        
        # Fallback 1: zkusíme poslední 2 znaky
        if len(name) >= 2:
            last_two = name[-2:]
            if last_two.isdigit():
                return int(last_two)
        
        # Fallback 2: zkusíme najít číslo za posledním podtržítkem
        parts = name.split('_')
        if parts:
            last_part = parts[-1]
            if last_part.isdigit():
                return int(last_part)
        
        return 0
    except Exception as e:
        print(f"Chyba při parsování čísla stránky z '{filename}': {e}")
        return 0

# Cesta k testovacím souborům
vzor_dir = Path(__file__).parent / "pdf-vzor"

print("=" * 80)
print("TEST PARSOVÁNÍ REÁLNÝCH SOUBORŮ Z pdf-vzor")
print("=" * 80)

# Ruční test na konkrétních příkladech
test_cases = [
    "PR25103001VY1.pdf",
    "PR25103002VY1.pdf",
    "PR25103003VY1.pdf",
    "PR25103004VY1.pdf",
    "PR25103005VY1.pdf",
    "PR25103006VY1.pdf",
    "PR25103007VY1.pdf",
    "PR25103008VY1.pdf",
]

print("\n📋 ANALÝZA NÁZVŮ:\n")
for filename in test_cases:
    name = Path(filename).stem
    page_num = parse_page_number(filename)
    parity = "sudá" if page_num % 2 == 0 else "lichá"
    
    # Ukážeme rozklad názvu
    if len(name) >= 13:
        pr = name[:2]
        date = name[2:8]
        page = name[8:10]
        version = name[10:]
        print(f"  {filename:25s}")
        print(f"    Rozklad: PR={pr} | Datum={date} | Strana={page} | Verze={version}")
        print(f"    Detekováno: Strana {page_num:2d} ({parity})")
        print()

# Test se soubory ze složky pdf-vzor (pokud existuje)
if vzor_dir.exists():
    print("\n" + "=" * 80)
    print("REÁLNÉ SOUBORY ZE SLOŽKY pdf-vzor")
    print("=" * 80)
    
    pdf_files = sorted(vzor_dir.glob("*.pdf"))
    
    if pdf_files:
        print(f"\nNalezeno {len(pdf_files)} PDF souborů:\n")
        
        file_data = []
        for pdf_file in pdf_files:
            page_num = parse_page_number(pdf_file.name)
            parity = "sudá" if page_num % 2 == 0 else "lichá"
            file_data.append({
                'name': pdf_file.name,
                'page': page_num,
                'parity': parity
            })
            print(f"  📄 {pdf_file.name:25s} → Strana {page_num:2d} ({parity})")
        
        # Analýza sudých/lichých
        even_pages = [f for f in file_data if f['page'] % 2 == 0 and f['page'] > 0]
        odd_pages = [f for f in file_data if f['page'] % 2 == 1]
        
        print("\n" + "=" * 80)
        print("ANALÝZA STRÁNEK")
        print("=" * 80)
        
        print(f"\n🔵 Sudé stránky (levá strana): {len(even_pages)}")
        for f in sorted(even_pages, key=lambda x: x['page']):
            print(f"   - Strana {f['page']:2d}: {f['name']}")
        
        print(f"\n🟢 Liché stránky (pravá strana): {len(odd_pages)}")
        for f in sorted(odd_pages, key=lambda x: x['page']):
            print(f"   - Strana {f['page']:2d}: {f['name']}")
        
        # Automatické párování
        print("\n" + "=" * 80)
        print("AUTOMATICKÉ PÁROVÁNÍ")
        print("=" * 80)
        
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
    else:
        print("\n❌ Žádné PDF soubory nenalezeny v složce pdf-vzor")
else:
    print("\n⚠️  Složka pdf-vzor neexistuje")

print("=" * 80)

