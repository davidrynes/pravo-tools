# PDF Merger - Spojování PDF souborů do dvoustrany

Aplikace pro spojování dvou PDF souborů do jedné dvoustrany s rotací a exportem s profilem PDF/X-1a:2001.

## 🎯 Funkce

- ✅ Spojení dvou PDF souborů do jedné dvoustrany
- ✅ Rotace o 90 stupňů (doleva nebo doprava) - **výchozí je -90° (doleva)**
- ✅ Export s profilem PDF/X-1a:2001
- ✅ **Automatická detekce čísla stránky z názvu souboru** 🆕
- ✅ Automatické rozpoznání sudých/lichých čísel stránek
- ✅ Vysoká kvalita výstupu (300 DPI)
- ✅ Podpora pro všechny PDF formáty
- 🆕 **Grafické rozhraní (GUI) s drag & drop podporou**
- 🆕 **Spustitelný soubor pro Windows/macOS/Linux**
- 🆕 **InDesign-like zpracování - zachovává textové informace**
- 🆕 **Nejmenší velikost souborů (1-3 MB místo 10-20 MB)**
- 🆕 **Dynamická rotace pro tiskárny novin - automaticky podle pořadí stránek**
- 🆕 **InDesign-like kvalita - zachovává textovou editovatelnost a vektorovou kvalitu**
- 🆕 **Webová aplikace s moderním rozhraním**
- 🆕 **Drag & drop podpora v prohlížeči**
- 🆕 **Real-time sledování zpracování**

## 🚀 Rychlé spuštění

### Webová aplikace (nejnovější - doporučeno)
```bash
# Spuštění webové aplikace
./start_web_app.sh

# Nebo přímo
source venv/bin/activate
python web_app.py
```
**Otevřete prohlížeč na adrese: http://localhost:8080**

### Grafické rozhraní (GUI)
```bash
# Spuštění InDesign-like GUI aplikace dvojklikem (macOS)
./PDF_Merger_InDesign.command

# Spuštění původní GUI aplikace dvojklikem (macOS)
./PDF_Merger.command

# Spuštění GUI aplikace dvojklikem (Windows)
PDF_Merger.bat

# Spuštění GUI aplikace z terminálu
./launch_gui.sh

# Nebo přímo
python3 pdf_merger_gui.py
```

### Vytvoření spustitelného souboru
```bash
# Vytvoření spustitelného souboru
./build.sh

# Spuštění vytvořeného souboru
./dist/PDF_Merger
```

### Příkazová řádka (CLI)
```bash
# InDesign-like verze (nejlepší - zachovává text, nejmenší soubory)
python indesign_like_pdf_merger.py --auto --mode indesign_like

# Text preserving verze (s textem, větší soubory)
python text_preserving_pdf_merger.py --auto --mode simple_text --dpi 300

# Professional verze (pro tiskárny)
python professional_pdf_merger.py --auto --mode compressed --dpi 300

# Minimal verze (nejmenší soubory, bez textu)
python optimized_pdf_merger.py --auto --mode minimal

# Původní verze
python advanced_pdf_merger.py --auto
```

## 📊 Porovnání verzí

| Verze | Velikost souborů | Text | Kvalita | Rychlost | Doporučení |
|-------|------------------|------|---------|----------|------------|
| **InDesign-like** | 1-3 MB | ✅ | Vysoká | Nejrychlejší | **Nejlepší** |
| Text preserving | 6-14 MB | ✅ | Vysoká | Rychlá | Pro tiskárny |
| Professional | 6-14 MB | ❌ | Vysoká | Rychlá | Pro tiskárny |
| Minimal | 1-2 MB | ❌ | Dobrá | Rychlá | Pro web |
| Původní | 10-20 MB | ❌ | Vysoká | Pomalá | Nepoužívat |

## 📋 Použití aplikací

### Webová aplikace
1. **Spuštění**: Spusťte `./start_web_app.sh` a otevřete http://localhost:8080
2. **Nahrání souborů**: Přetáhněte PDF soubory do drag & drop oblasti
3. **Automatické párování**: Klikněte na "Automatické párování" nebo vytvořte vlastní páry
4. **Ruční párování**: Přetáhněte soubory z levé strany do pravé pro vytvoření vlastních párů
5. **Spuštění**: Klikněte na "Spustit slučování" (rotace je automatická pro tiskárny)
6. **Stažení**: Stáhněte vytvořené soubory

### GUI aplikace
1. **Nahrání souborů**: Klikněte na "Vybrat PDF soubory" nebo přetáhněte soubory do aplikace
2. **Automatické párování**: Aplikace automaticky spáruje soubory podle čísel (sudé = levá, liché = pravá)
3. **Ruční úprava**: Můžete přidat/upravit/odstranit páry pomocí kontextového menu
4. **Nastavení**: Vyberte rotaci (-90° nebo +90°) a kvalitu (DPI)
5. **Spuštění**: Klikněte na "Sloučit PDF soubory"

## 🖨️ Dynamická rotace pro oboustranný tisk

Aplikace **automaticky aplikuje správnou rotaci** pro oboustranný tisk v tiskárnách:

### 📐 Logika rotace:
- **Levá stránka SUDÁ** (2, 4, 6...): **+90°** (doprava) ↻ → **Přední strana listu**
- **Levá stránka LICHÁ** (3, 5, 7...): **-90°** (doleva) ↺ → **Zadní strana listu**
- **Zachovává kvalitu**: InDesign-like přístup s přímým kopírováním PDF objektů
- **Textová editovatelnost**: Zachována pro vyhledávání a kopírování

### 📊 Příklady pro oboustranný tisk:
| Pár | Levá | Pravá | Typ | Rotace | Po otočení |
|-----|------|-------|-----|--------|------------|
| 2-3 | 2 (S) | 3 (L) | Přední | **+90°** ↻ | Správně orientováno |
| 3-4 | 3 (L) | 4 (S) | Zadní | **-90°** ↺ | Správně orientováno |
| 4-5 | 4 (S) | 5 (L) | Přední | **+90°** ↻ | Správně orientováno |
| 5-6 | 5 (L) | 6 (S) | Zadní | **-90°** ↺ | Správně orientováno |
| 6-7 | 6 (S) | 7 (L) | Přední | **+90°** ↻ | Správně orientováno |
| 7-8 | 7 (L) | 8 (S) | Zadní | **-90°** ↺ | Správně orientováno |

### 🖨️ Proces v tiskárně:
```
LIST 1: Přední (2-3) +90° ↻  |  Zadní (3-4) -90° ↺
LIST 2: Přední (4-5) +90° ↻  |  Zadní (5-6) -90° ↺  
LIST 3: Přední (6-7) +90° ↻  |  Zadní (7-8) -90° ↺
```

**Toto zajišťuje, že po oboustranném tisku a složení budou všechny strany správně orientované! ✅**

## 🔄 InDesign-like přístup

Aplikace používá InDesign-like přístup pro maximální kvalitu:

1. **Přímé kopírování**: PDF objekty se kopírují přímo bez konverze na obrázky
2. **Zachování textu**: Text zůstává editovatelný a vyhledatelný
3. **Vektorová kvalita**: Zachována pro ostrý tisk
4. **Optimalizace**: Komprese a vyčištění pro menší velikost

**Výhody:**
- ✅ Správná orientace pro tiskárny novin
- ✅ Text zůstává vyhledatelný a kopírovatelný
- ✅ Vysoká kvalita tisku (vektorová)
- ✅ Optimalizovaná velikost (3-4 MB)

## 💻 Příkazová řádka

### Automatické spojení všech párových souborů
```bash
python advanced_pdf_merger.py --auto
```

### Spojení konkrétních souborů
```bash
python advanced_pdf_merger.py --left PRAVO_NEW_TEST03_FINAL_02.pdf --right PRAVO_NEW_TEST03_FINAL_03.pdf --output merged_02_03.pdf
```

### Rotace doprava místo doleva
```bash
python advanced_pdf_merger.py --auto --rotation 90
```

### Vyšší kvalita (600 DPI)
```bash
python advanced_pdf_merger.py --auto --dpi 600
```

## Struktura projektu

```
pdf-merge/
├── files/                          # Vstupní PDF soubory
│   ├── PRAVO_NEW_TEST03_FINAL_02.pdf
│   ├── PRAVO_NEW_TEST03_FINAL_03.pdf
│   ├── PRAVO_NEW_TEST03_FINAL_14.pdf
│   ├── PRAVO_NEW_TEST03_FINAL_15.pdf
│   ├── Test03_02.pdf
│   └── Test03_03.pdf
├── output/                         # Výstupní spojené PDF soubory
├── pdf_merger.py                   # Základní verze (CLI)
├── advanced_pdf_merger.py          # Pokročilá verze (CLI)
├── pdf_merger_gui.py               # GUI aplikace 🆕
├── PDF_Merger.command              # Spustitelná aplikace pro macOS 🆕
├── PDF_Merger.bat                  # Spustitelná aplikace pro Windows 🆕
├── PDF_Merger.py                   # Python launcher s auto-instalací 🆕
├── pdf_merger.spec                 # PyInstaller spec soubor
├── build.sh                        # Build script pro spustitelný soubor
├── build_macos.sh                  # Build script pro macOS aplikaci
├── launch_gui.sh                   # Launcher pro GUI
├── run.sh                          # Interaktivní CLI launcher
├── requirements.txt                # Závislosti
└── README.md                       # Tento soubor
```

## Jak to funguje

1. **Automatická detekce čísla stránky**: Aplikace detekuje číslo stránky přímo z názvu souboru
   - Podporuje formát: `PRYYMMDDXXBBB.pdf` (extrahuje poslední 2 číslice XX)
   - Příklad: `PRAVO_NEW_TEST03_FINAL_02.pdf` → Strana 02
   - Fallback: `název_číslo.pdf` → extrahuje číslo za posledním podtržítkem
   - **Více informací**: viz [STRÁNKY_INFO.md](STRÁNKY_INFO.md)

2. **Rozpoznání párových souborů**: Aplikace automaticky rozpozná páry podle čísel stránek
   - Sudé číslo (02, 04, 14) = levá stránka
   - Liché číslo (03, 05, 15) = pravá stránka

3. **Konverze na obrázky**: PDF soubory se konvertují na vysokokvalitní obrázky (300 DPI)

4. **Spojení**: Obrázky se spojí vedle sebe do jednoho obrázku

5. **Rotace**: Výsledný obrázek se otočí o 90 stupňů (automaticky podle pořadí stránek)

6. **Export**: Obrázek se exportuje jako PDF s profilem PDF/X-1a:2001

## Výstup

Výsledné PDF soubory budou uloženy ve složce `output/` s názvy:
- `merged_02_03.pdf` (pro soubory s čísly 02 a 03)
- `merged_14_15.pdf` (pro soubory s čísly 14 a 15)
- atd.

## Požadavky

- Python 3.7+
- PyPDF2
- reportlab
- Pillow
- PyMuPDF

## Poznámky

- Aplikace automaticky vytvoří složku `output/` pokud neexistuje
- Všechny operace jsou logovány do konzole
- Podporuje pouze PDF soubory s jednou stránkou
- Výstupní PDF má vysokou kvalitu díky konverzi přes obrázky
