# 🖨️ Oboustranný Tisk - Rotace PDF

## 🎯 Problém a Řešení

### ❌ Problém (původní implementace):
Páry **2-3** a **3-4** byly otočeny **stejným směrem**, což způsobovalo problémy při oboustranném tisku.

### ✅ Řešení (nová implementace):
Rotace je nyní založena na **pozici levé stránky** (sudá vs lichá), což zajišťuje správnou orientaci pro oboustranný tisk.

---

## 📐 Jednoduchá Logika

```python
if left_page % 2 == 0:  # Levá stránka je SUDÁ
    rotation = +90°     # Přední strana listu ↻
else:                    # Levá stránka je LICHÁ
    rotation = -90°     # Zadní strana listu ↺
```

---

## 📊 Vizualizace Oboustranného Tisku

### LIST 1

```
┌────────────────────────────────────────────────────────────┐
│                         LIST 1                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  PŘEDNÍ STRANA:                                            │
│  ┌─────────┬─────────┐                                    │
│  │ Strana 2│ Strana 3│  → Rotace +90° ↻                  │
│  │  (sudá) │ (lichá) │                                    │
│  └─────────┴─────────┘                                    │
│                                                            │
│  Po otočení o +90° doprava:                                │
│  ┌──────────────┐                                         │
│  │      │       │                                         │
│  │   3  │   2   │  ← Správně orientováno                 │
│  │      │       │                                         │
│  └──────────────┘                                         │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ZADNÍ STRANA (druhá strana listu):                        │
│  ┌─────────┬─────────┐                                    │
│  │ Strana 3│ Strana 4│  → Rotace -90° ↺                  │
│  │ (lichá) │  (sudá) │                                    │
│  └─────────┴─────────┘                                    │
│                                                            │
│  Po otočení o -90° doleva:                                 │
│  ┌──────────────┐                                         │
│  │      │       │                                         │
│  │   4  │   3   │  ← Správně orientováno                 │
│  │      │       │                                         │
│  └──────────────┘                                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### LIST 2

```
┌────────────────────────────────────────────────────────────┐
│                         LIST 2                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  PŘEDNÍ: Pár 4-5 (levá sudá) → +90° ↻                    │
│  ZADNÍ:  Pár 5-6 (levá lichá) → -90° ↺                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### LIST 3

```
┌────────────────────────────────────────────────────────────┐
│                         LIST 3                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  PŘEDNÍ: Pár 6-7 (levá sudá) → +90° ↻                    │
│  ZADNÍ:  Pár 7-8 (levá lichá) → -90° ↺                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 📋 Kompletní Tabulka

| Pár | Levá | Pravá | Levá je | Rotace | Strana listu | Po složení |
|-----|------|-------|---------|--------|--------------|------------|
| 2-3 | 2 | 3 | Sudá | **+90°** ↻ | Přední | ✅ OK |
| 3-4 | 3 | 4 | Lichá | **-90°** ↺ | Zadní | ✅ OK |
| 4-5 | 4 | 5 | Sudá | **+90°** ↻ | Přední | ✅ OK |
| 5-6 | 5 | 6 | Lichá | **-90°** ↺ | Zadní | ✅ OK |
| 6-7 | 6 | 7 | Sudá | **+90°** ↻ | Přední | ✅ OK |
| 7-8 | 7 | 8 | Lichá | **-90°** ↺ | Zadní | ✅ OK |

---

## 🔄 Proces v Tiskárně

```
┌─────────────────────────────────────────────────────────────────┐
│                    OBOUSTRANNÝ TISK                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  KROK 1: Vytvoření PDF párů                                     │
│    ✅ 2-3 (přední) - otočeno +90° ↻                            │
│    ✅ 3-4 (zadní)  - otočeno -90° ↺                            │
│    ✅ 4-5 (přední) - otočeno +90° ↻                            │
│    ✅ 5-6 (zadní)  - otočeno -90° ↺                            │
│                                                                 │
│  KROK 2: Tisk v tiskárně                                        │
│    → Tisk přední strany (2-3, 4-5, 6-7...)                     │
│    → Otočení papíru                                             │
│    → Tisk zadní strany (3-4, 5-6, 7-8...)                      │
│                                                                 │
│  KROK 3: Složení                                                │
│    → Všechny strany jsou správně orientované! ✅               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Implementace

### V `web_app.py`:

```python
# Dynamická rotace pro oboustranný tisk
if left_page % 2 == 0:  # Levá je sudá → Přední strana
    rotation = 90
    logger.info(f"Přední strana ({left_page}-{right_page}): Rotace +90°")
else:  # Levá je lichá → Zadní strana
    rotation = -90
    logger.info(f"Zadní strana ({left_page}-{right_page}): Rotace -90°")

success = self.merger.create_side_by_side_pdf_with_rotation(
    left_file_path, right_file_path, output_path, rotation
)
```

---

## 🎯 Proč Tato Logika Funguje?

### Klíčové poznatky:

1. **Oboustranný tisk = 2 různé orientace**
   - Přední strana potřebuje jednu rotaci
   - Zadní strana potřebuje opačnou rotaci

2. **Pozice levé stránky určuje typ**
   - Levá SUDÁ (2, 4, 6) = Vždy PŘEDNÍ strana
   - Levá LICHÁ (3, 5, 7) = Vždy ZADNÍ strana

3. **Univerzální řešení**
   - Funguje pro **jakékoli páry**
   - Nevyžaduje **žádnou konfiguraci**
   - Automaticky **správná rotace**

---

## 🧪 Testování

Pro ověření správnosti spusťte:

```bash
python test_final_rotation.py
```

**Výstup ukáže:**
```
✅ Pár 2-3: Přední strana → Rotace: +90°
✅ Pár 3-4: Zadní strana  → Rotace: -90°
✅ Pár 4-5: Přední strana → Rotace: +90°
✅ Pár 5-6: Zadní strana  → Rotace: -90°
✅ VŠECHNY TESTY PROŠLY!
```

---

## ❌ Co NEFUNGOVALO (původní implementace)

### Pokus 1: Porovnání left < right
```python
if left_page < right_page:
    rotation = +90°
else:
    rotation = -90°
```
**Problém:** Páry 2-3 a 4-5 měly stejnou rotaci, ale i pár 3-4 měl stejnou!

### Pokus 2: Porovnání lichá vs sudá
```python
if odd_page > even_page:
    rotation = +90°
else:
    rotation = -90°
```
**Problém:** Složitější logika, ale stále nefungovala pro oboustranný tisk.

### ✅ Finální řešení: Pozice levé stránky
```python
if left_page % 2 == 0:  # Levá je sudá
    rotation = +90°     # Přední
else:                    # Levá je lichá
    rotation = -90°     # Zadní
```
**Výhoda:** Jednoduché, spolehlivé, funguje pro oboustranný tisk! ✅

---

## 📝 Poznámky

### ⚠️ Důležité pro uživatele:

1. **Automatické párování vytvoří pouze páry typu 2-3, 4-5, 6-7** (sudá-lichá)
   - Tyto páry budou všechny otočeny **+90°** ↻

2. **Pro zadní strany (3-4, 5-6, 7-8) musíte vytvořit páry manuálně**
   - Drag & drop v UI
   - Tyto páry budou automaticky otočeny **-90°** ↺

3. **Aplikace automaticky rozpozná typ páru podle levé stránky**
   - Žádná manuální konfigurace rotace není potřeba!

---

## 🎨 ASCII Art Vizualizace

### Přední strana (2-3):
```
Před:           Po rotaci +90° ↻:
┌───┬───┐       ┌────────┐
│ 2 │ 3 │   →   │   │    │
└───┴───┘       │ 3 │ 2  │
                │   │    │
                └────────┘
```

### Zadní strana (3-4):
```
Před:           Po rotaci -90° ↺:
┌───┬───┐       ┌────────┐
│ 3 │ 4 │   →   │   │    │
└───┴───┘       │ 4 │ 3  │
                │   │    │
                └────────┘
```

---

**Autor:** David Rynes  
**Verze:** 3.0 (Finální oprava pro oboustranný tisk)  
**Datum:** Říjen 2025  
**Status:** ✅ FUNKČNÍ - Otestováno na reálných souborech

