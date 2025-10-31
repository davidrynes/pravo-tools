# 📰 Oboustranný Tisk Dvojstran (Novinový Tisk)

## 🎯 Konečné Řešení

### ✅ SPRÁVNÁ Logika:

**Rotace závisí na POŘADÍ PÁRU v seznamu!**

```python
for i, pair in enumerate(file_pairs, start=1):  # 1-based pořadí
    if i % 2 == 1:  # Liché pořadí (1, 3, 5...)
        rotation = +90°  # Přední strana papíru
    else:           # Sudé pořadí (2, 4, 6...)
        rotation = -90°  # Zadní strana papíru
```

---

## 📐 Princip Oboustranného Tisku Dvojstran

### Co je "dvojstrana"?
- **Dvojstrana** = 2 PDF stránky spojené vedle sebe
- Každé PDF se používá **pouze jednou**
- Tiskárna tiskne dvojstranu na **jeden fyzický papír oboustranně**

### Příklad:
```
PAPÍR 1:
  PŘEDNÍ STRANA: 1. pár (PDF 2 + PDF 3) → Rotace +90° ↻
  [Papír se otočí]
  ZADNÍ STRANA:  2. pár (PDF 4 + PDF 5) → Rotace -90° ↺
```

---

## 📊 Kompletní Příklad

| Fyzický papír | Strana | Pořadí páru | PDF | Rotace | Vysvětlení |
|---------------|--------|-------------|-----|--------|------------|
| **PAPÍR 1** | Přední | 1. pár | 2-3 | **+90°** ↻ | První pár v seznamu |
| **PAPÍR 1** | Zadní | 2. pár | 4-5 | **-90°** ↺ | Druhý pár v seznamu |
| **PAPÍR 2** | Přední | 3. pár | 6-7 | **+90°** ↻ | Třetí pár v seznamu |
| **PAPÍR 2** | Zadní | 4. pár | 8-9 | **-90°** ↺ | Čtvrtý pár v seznamu |
| **PAPÍR 3** | Přední | 5. pár | 10-11 | **+90°** ↻ | Pátý pár v seznamu |
| **PAPÍR 3** | Zadní | 6. pár | 12-13 | **-90°** ↺ | Šestý pár v seznamu |

---

## 🖨️ Proces v Tiskárně

### Krok za krokem:

```
┌──────────────────────────────────────────────────────────┐
│                      PAPÍR 1                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  KROK 1: Tisk přední strany                              │
│    ✅ Vezme 1. pár (PDF 2-3)                            │
│    ✅ Otočí o +90° ↻                                     │
│    ✅ Vytiskne na PŘEDNÍ stranu papíru                   │
│                                                          │
│  KROK 2: Otočení papíru                                  │
│    → Papír se v tiskárně otočí                           │
│                                                          │
│  KROK 3: Tisk zadní strany                               │
│    ✅ Vezme 2. pár (PDF 4-5)                            │
│    ✅ Otočí o -90° ↺                                     │
│    ✅ Vytiskne na ZADNÍ stranu papíru                    │
│                                                          │
│  → PAPÍR 1 je hotový! ✅                                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                      PAPÍR 2                             │
├──────────────────────────────────────────────────────────┤
│  PŘEDNÍ: 3. pár (PDF 6-7)  → +90° ↻                     │
│  ZADNÍ:  4. pár (PDF 8-9)  → -90° ↺                     │
│  → PAPÍR 2 je hotový! ✅                                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                      PAPÍR 3                             │
├──────────────────────────────────────────────────────────┤
│  PŘEDNÍ: 5. pár (PDF 10-11) → +90° ↻                    │
│  ZADNÍ:  6. pár (PDF 12-13) → -90° ↺                    │
│  → PAPÍR 3 je hotový! ✅                                │
└──────────────────────────────────────────────────────────┘
```

---

## 💻 Implementace v Kódu

### V `web_app.py`:

```python
def merge_files(self, file_pairs: list, rotation: int = -90) -> dict:
    """Spojí páry PDF souborů"""
    results = {
        'success': [],
        'errors': [],
        'total_files': len(file_pairs)
    }
    
    for i, pair in enumerate(file_pairs, start=1):  # start=1 pro 1-based pořadí
        try:
            left_file = pair['left_file']
            right_file = pair['right_file']
            
            # OBOUSTRANNÝ TISK DVOJSTRAN:
            # Rotace závisí na POŘADÍ PÁRU (liché = přední, sudé = zadní)
            if i % 2 == 1:  # Liché pořadí (1, 3, 5...) = Přední strana
                rotation = 90
                side = "Přední"
            else:  # Sudé pořadí (2, 4, 6...) = Zadní strana
                rotation = -90
                side = "Zadní"
            
            logger.info(f"{i}. pár ({left_page}-{right_page}): {side} strana → Rotace {rotation}°")
            
            # Vytvoření spojeného PDF s rotací
            success = self.merger.create_side_by_side_pdf_with_rotation(
                left_file_path, right_file_path, output_path, rotation
            )
```

---

## 🔍 Proč Toto Funguje?

### Klíčové poznatky:

1. **Pořadí párů určuje stránku papíru**
   - První pár = Přední strana prvního papíru
   - Druhý pár = Zadní strana prvního papíru
   - Třetí pár = Přední strana druhého papíru
   - atd.

2. **Každé PDF použito pouze jednou**
   - PDF 2 je pouze v 1. páru
   - PDF 3 je pouze v 1. páru
   - PDF 4 je pouze v 2. páru
   - PDF 5 je pouze v 2. páru
   - **Žádné PDF se neopakuje!**

3. **Střídavá rotace**
   - Přední strany: +90° (všechny stejně)
   - Zadní strany: -90° (všechny stejně)
   - Ale střídavě podle pořadí!

---

## ❌ Co NEFUNGOVALO (předchozí pokusy)

### Pokus 1: Všechny páry stejná rotace
```python
rotation = -90  # Všechny stejně
```
**Problém:** Páry 2-3 a 4-5 obě -90°, ale jsou na opačných stranách papíru!

### Pokus 2: Podle levé stránky (sudá/lichá)
```python
if left_page % 2 == 0:
    rotation = +90
else:
    rotation = -90
```
**Problém:** Funguje pro první papír, ale ne pro další!

### Pokus 3: Podle porovnání lichá vs sudá
```python
if odd_page > even_page:
    rotation = +90
else:
    rotation = -90
```
**Problém:** Složitější, ale stále nefunguje pro oboustranný tisk!

### ✅ Finální řešení: Podle pořadí páru
```python
if i % 2 == 1:  # Liché pořadí
    rotation = +90  # Přední
else:           # Sudé pořadí
    rotation = -90  # Zadní
```
**Výhoda:** Jednoduché, univerzální, funguje pro oboustranný tisk dvojstran! ✅

---

## 🎯 Jak Používat Aplikaci

### 1. Nahrání PDF
- Nahrajte všechny PDF soubory (2, 3, 4, 5, 6, 7, 8, 9...)

### 2. Vytvoření párů
- **Auto-párování:** Vytvoří páry 2-3, 4-5, 6-7, 8-9...
- **Důležité:** Pořadí párů určuje rotaci!

### 3. Kontrola pořadí
Zkontrolujte, že páry jsou ve správném pořadí:
```
1. pár: 2-3  (bude přední strana papíru 1)
2. pár: 4-5  (bude zadní strana papíru 1)
3. pár: 6-7  (bude přední strana papíru 2)
4. pár: 8-9  (bude zadní strana papíru 2)
```

### 4. Spojení
- Klikněte "Spojit PDF"
- Aplikace automaticky aplikuje správnou rotaci podle pořadí

### 5. Tisk
- Stáhněte spojené PDF
- Pošlete do tiskárny
- Tiskárna vytiskne oboustranně
- Po složení: Všechny strany správně orientované! ✅

---

## 📝 Důležité Poznámky

### ⚠️ Pořadí párů je KLÍČOVÉ!

Pokud změníte pořadí párů, změní se rotace:
- Přesunete pár 4-5 na 1. místo → Dostane +90° místo -90° ❌
- Musíte udržet správné pořadí!

### ✅ Auto-párování

Auto-párování vytvoří páry ve správném pořadí:
1. Najde sudé a liché stránky
2. Spáruje je (2-3, 4-5, 6-7...)
3. Seřadí je podle čísel stránek
4. Aplikace pak aplikuje rotaci podle pořadí

### 🎯 Pro speciální případy

Pokud potřebujete jiné pořadí (např. zadní strany novin):
1. Vytvořte páry manuálně (drag & drop)
2. Seřaďte je v požadovaném pořadí
3. Aplikace použije rotaci podle pořadí v seznamu

---

## 🧪 Testování

Pro ověření správnosti:

```bash
python test_correct_newspaper_logic.py
```

**Výstup:**
```
✅ Pár 2-3 (1. pár): Přední strana papíru 1 → +90°
✅ Pár 4-5 (2. pár): Zadní strana papíru 1  → -90°
✅ Pár 6-7 (3. pár): Přední strana papíru 2 → +90°
✅ Pár 8-9 (4. pár): Zadní strana papíru 2  → -90°
✅ VŠECHNY TESTY PROŠLY!
```

---

## 📚 ASCII Art Vizualizace

### Papír 1 - Přední strana (1. pár):
```
PDF 2-3 před:        Po rotaci +90° ↻:
┌───┬───┐           ┌────────┐
│ 2 │ 3 │    →      │   │    │
└───┴───┘           │ 3 │ 2  │
                    │   │    │
                    └────────┘
```

### Papír 1 - Zadní strana (2. pár):
```
PDF 4-5 před:        Po rotaci -90° ↺:
┌───┬───┐           ┌────────┐
│ 4 │ 5 │    →      │   │    │
└───┴───┘           │ 5 │ 4  │
                    │   │    │
                    └────────┘
```

### Po složení:
```
Papír 1 hotový:
  Přední: [3 | 2] (otočeno +90°)
  Zadní:  [5 | 4] (otočeno -90°)
  → Po složení správně orientováno! ✅
```

---

**Autor:** David Rynes  
**Verze:** 4.0 (Finální - Rotace podle pořadí páru)  
**Datum:** Říjen 2025  
**Status:** ✅ FUNKČNÍ - Testováno pro oboustranný tisk dvojstran

---

**🎉 KONEČNĚ SPRÁVNĚ! Rotace podle pořadí páru funguje pro oboustranný tisk dvojstran!**

