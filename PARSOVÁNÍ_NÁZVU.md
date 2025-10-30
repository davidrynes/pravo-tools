# 🔍 Parsování Čísla Stránky z Názvu Souboru

## 📐 Vizuální Diagram

### Formát: `PRYYMMDDXXBBB.pdf`

```
┌──────────────────────────────────────────────────────────┐
│                    PR25103001VY1.pdf                      │
└──────────────────────────────────────────────────────────┘
    │  │    │  │  │                │ │ │
    │  │    │  │  │                │ │ └─── .pdf (přípona)
    │  │    │  │  │                │ └───── B (3. znak verze)
    │  │    │  │  │                └─────── B (2. znak verze)
    │  │    │  │  │                        B (1. znak verze) = "VY1"
    │  │    │  │  │
    │  │    │  │  └──────────────────────── X (číslo stránky - 2. číslice) = "1"
    │  │    │  └─────────────────────────── X (číslo stránky - 1. číslice) = "0"
    │  │    │
    │  │    └────────────────────────────── DD (den) = "30"
    │  └─────────────────────────────────── MM (měsíc) = "10"
    └────────────────────────────────────── YY (rok) = "25" + PR (prefix) = "PR"
```

---

## 📊 Extrakce v Pythonu

### Pozice znaků (od konce)

```python
name = "PR25103001VY1"

Position:  P  R  2  5  1  0  3  0  0  1  V  Y  1
Index:     0  1  2  3  4  5  6  7  8  9 10 11 12
From end: -13-12-11-10 -9 -8 -7 -6 -5 -4 -3 -2 -1

Číslo stránky: name[-5:-3] = "01"
               ▲    ▲
               │    │
          Pozice -5  Pozice -3 (exclusive)
```

---

## 🎯 Příklady Extrakce

### Příklad 1: Strana 01

```
Soubor: PR25103001VY1.pdf

┌─────────────┬──────────┬────────┬─────────┐
│   Prefix    │  Datum   │ Strana │  Verze  │
│   + YY      │  MMDD    │   XX   │   BBB   │
├─────────────┼──────────┼────────┼─────────┤
│  PR + 25    │   1030   │   01   │   VY1   │
└─────────────┴──────────┴────────┴─────────┘
                            ▲▲
                            ││
                     name[-5:-3] = "01"

Výsledek: Strana 01 → Lichá 🟢
```

### Příklad 2: Strana 02

```
Soubor: PR25103002VY1.pdf

┌─────────────┬──────────┬────────┬─────────┐
│   Prefix    │  Datum   │ Strana │  Verze  │
│   + YY      │  MMDD    │   XX   │   BBB   │
├─────────────┼──────────┼────────┼─────────┤
│  PR + 25    │   1030   │   02   │   VY1   │
└─────────────┴──────────┴────────┴─────────┘
                            ▲▲
                            ││
                     name[-5:-3] = "02"

Výsledek: Strana 02 → Sudá 🔵
```

### Příklad 3: Strana 40

```
Soubor: PR25103040VY1.pdf

┌─────────────┬──────────┬────────┬─────────┐
│   Prefix    │  Datum   │ Strana │  Verze  │
│   + YY      │  MMDD    │   XX   │   BBB   │
├─────────────┼──────────┼────────┼─────────┤
│  PR + 25    │   1030   │   40   │   VY1   │
└─────────────┴──────────┴────────┴─────────┘
                            ▲▲
                            ││
                     name[-5:-3] = "40"

Výsledek: Strana 40 → Sudá 🔵
```

---

## 💻 Python Implementace

```python
from pathlib import Path

def parse_page_number(filename: str) -> int:
    """
    Extrahuje číslo stránky z názvu souboru.
    
    Formát: PRYYMMDDXXBBB.pdf
    - XX je na pozici [-5:-3] (4. a 5. znak od konce)
    """
    name = Path(filename).stem
    
    # Extrakce XX (4. a 5. znak od konce)
    if len(name) >= 5:
        page_chars = name[-5:-3]
        if page_chars.isdigit():
            return int(page_chars)
    
    return 0

# Testování
test_files = [
    "PR25103001VY1.pdf",  # Strana 01
    "PR25103002VY1.pdf",  # Strana 02
    "PR25103040VY1.pdf",  # Strana 40
]

for filename in test_files:
    page = parse_page_number(filename)
    parity = "lichá 🟢" if page % 2 == 1 else "sudá 🔵"
    print(f"{filename:25s} -> Strana {page:2d} ({parity})")
```

**Výstup:**
```
PR25103001VY1.pdf         -> Strana  1 (lichá 🟢)
PR25103002VY1.pdf         -> Strana  2 (sudá 🔵)
PR25103040VY1.pdf         -> Strana 40 (sudá 🔵)
```

---

## 🔄 Proces v Aplikaci

```
┌─────────────────────────────────────────────────────┐
│  1. Uživatel nahraje: PR25103002VY1.pdf             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  2. parse_page_number("PR25103002VY1.pdf")          │
│     → name = "PR25103002VY1"                        │
│     → page_chars = name[-5:-3] = "02"               │
│     → return int("02") = 2                          │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  3. Klasifikace: 2 % 2 == 0 → Sudá stránka 🔵      │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  4. UI: Modrý badge "Sudá"                          │
│     → Zobrazit v seznamu levých stránek             │
└─────────────────────────────────────────────────────┘
```

---

## 🧪 Testování

Pro ověření správné detekce spusťte:

```bash
python test_vzor_files.py
```

Tento skript:
1. ✅ Analyzuje všechny PDF v `pdf-vzor/`
2. ✅ Zobrazí rozklad názvu souboru
3. ✅ Ověří správnost detekce čísla stránky
4. ✅ Ukáže automatické párování
5. ✅ Určí správnou rotaci

---

## 📝 Poznámky

### ✅ Podporované Formáty

1. **PRYYMMDDXXBBB.pdf** (primární)
   - `PR25103001VY1.pdf` → Strana 01

2. **název_XX.pdf** (fallback)
   - `PRAVO_NEW_TEST03_FINAL_02.pdf` → Strana 02

3. **názvěXX.pdf** (fallback)
   - `document15.pdf` → Strana 15

### ⚠️ Omezení

- Číslo stránky musí být **2 znaky** (01-99)
- Pro stránky > 99 je potřeba upravit formát
- Poslední 3 znaky (BBB) nesmí být číslice

---

## 🎨 UI Vizualizace

```
┌─────────────────────────────────────────────────────────┐
│  📄 PR25103001VY1.pdf              🟢 Lichá            │
│     Stránka: 01 | Velikost: 1.7 MB | Nahráno: 12:34   │
├─────────────────────────────────────────────────────────┤
│  📄 PR25103002VY1.pdf              🔵 Sudá             │
│     Stránka: 02 | Velikost: 1.0 MB | Nahráno: 12:34   │
├─────────────────────────────────────────────────────────┤
│  📄 PR25103003VY1.pdf              🟢 Lichá            │
│     Stránka: 03 | Velikost: 1.7 MB | Nahráno: 12:34   │
└─────────────────────────────────────────────────────────┘
```

---

**Autor:** David Rynes  
**Verze:** 2.1  
**Datum:** Říjen 2025

