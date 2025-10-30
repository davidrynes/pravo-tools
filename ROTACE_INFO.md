# 🔄 Dynamická Rotace - Podrobný Popis

## 🎯 Základní Princip

Aplikace **automaticky určuje rotaci** podle vztahu mezi **lichými a sudými stránkami**.

### 📐 Pravidlo:
```
┌─────────────────────────────────────────────────┐
│  POKUD lichá > sudá  →  Rotace +90° (doprava) ↻ │
│  POKUD lichá < sudá  →  Rotace -90° (doleva)  ↺ │
└─────────────────────────────────────────────────┘
```

---

## 📊 Vizuální Příklady

### Příklad 1: Přední strany (2-3)

```
┌──────────────────────┐     ┌──────────────────────┐
│                      │     │                      │
│   Strana 2 (sudá)    │  +  │   Strana 3 (lichá)   │
│                      │     │                      │
└──────────────────────┘     └──────────────────────┘

Výpočet:
  Lichá: 3
  Sudá:  2
  Porovnání: 3 > 2
  
  → Rotace: +90° (doprava) ↻

Výsledek:
     ┌──────────────────────────────────────┐
     │                                      │
     │  [Strana 2]      [Strana 3]         │
     │                                      │
     └──────────────────────────────────────┘
              Otočeno o +90° →
```

---

### Příklad 2: Zadní strany (40-39)

```
┌──────────────────────┐     ┌──────────────────────┐
│                      │     │                      │
│   Strana 40 (sudá)   │  +  │   Strana 39 (lichá)  │
│                      │     │                      │
└──────────────────────┘     └──────────────────────┘

Výpočet:
  Lichá: 39
  Sudá:  40
  Porovnání: 39 < 40
  
  → Rotace: -90° (doleva) ↺

Výsledek:
     ┌──────────────────────────────────────┐
     │                                      │
     │  [Strana 40]     [Strana 39]        │
     │                                      │
     └──────────────────────────────────────┘
              Otočeno o -90° ←
```

---

## 📋 Kompletní Tabulka Všech Kombinací

| Pár | Levá | Pravá | Lichá | Sudá | Porovnání | Rotace | Použití |
|-----|------|-------|-------|------|-----------|--------|---------|
| 2-3 | 2 (S) | 3 (L) | 3 | 2 | 3 > 2 | **+90° ↻** | Přední strany |
| 4-5 | 4 (S) | 5 (L) | 5 | 4 | 5 > 4 | **+90° ↻** | Přední strany |
| 6-7 | 6 (S) | 7 (L) | 7 | 6 | 7 > 6 | **+90° ↻** | Přední strany |
| 40-39 | 40 (S) | 39 (L) | 39 | 40 | 39 < 40 | **-90° ↺** | Zadní strany |
| 38-37 | 38 (S) | 37 (L) | 37 | 38 | 37 < 38 | **-90° ↺** | Zadní strany |
| 1-2 | 1 (L) | 2 (S) | 1 | 2 | 1 < 2 | **-90° ↺** | Nepárné |
| 3-2 | 3 (L) | 2 (S) | 3 | 2 | 3 > 2 | **+90° ↻** | Nepárné |
| 5-4 | 5 (L) | 4 (S) | 5 | 4 | 5 > 4 | **+90° ↻** | Nepárné |

*(S) = Sudá, (L) = Lichá*

---

## 💻 Implementace v Kódu

```python
# Zjistíme, která stránka je lichá a která sudá
if left_page % 2 == 0:  # Levá je sudá
    odd_page = right_page
    even_page = left_page
else:  # Levá je lichá
    odd_page = left_page
    even_page = right_page

# Logika: Pokud liché > sudé: +90°, Pokud liché < sudé: -90°
if odd_page > even_page:
    rotation = 90  # +90° (doprava) ↻
else:
    rotation = -90  # -90° (doleva) ↺
```

---

## 🔍 Krok za Krokem

### Scénář 1: Pár 2-3

```
1. Identifikace:
   left_page = 2 (sudá)
   right_page = 3 (lichá)

2. Určení lichá/sudá:
   2 % 2 == 0  →  Levá je sudá
   odd_page = 3
   even_page = 2

3. Porovnání:
   3 > 2  →  True

4. Rotace:
   odd_page > even_page  →  +90° ↻
```

---

### Scénář 2: Pár 40-39

```
1. Identifikace:
   left_page = 40 (sudá)
   right_page = 39 (lichá)

2. Určení lichá/sudá:
   40 % 2 == 0  →  Levá je sudá
   odd_page = 39
   even_page = 40

3. Porovnání:
   39 < 40  →  True

4. Rotace:
   odd_page < even_page  →  -90° ↺
```

---

## 🎨 Vizualizace Rotace

### +90° (Doprava) ↻

```
PŘED:                        PO ROTACI:
┌─────┬─────┐               ┌──────────────┐
│  2  │  3  │               │      │       │
│     │     │      →        │   3  │   2   │
└─────┴─────┘               │      │       │
                            └──────────────┘
   Horizontální              Vertikální (otočeno +90°)
```

### -90° (Doleva) ↺

```
PŘED:                        PO ROTACI:
┌─────┬─────┐               ┌──────────────┐
│ 40  │ 39  │               │      │       │
│     │     │      →        │  39  │  40   │
└─────┴─────┘               │      │       │
                            └──────────────┘
   Horizontální              Vertikální (otočeno -90°)
```

---

## 🖨️ Proč Tato Logika?

### 📰 Tiskařský Standard

V tiskárnách novin:
- **Přední strany**: 2-3, 4-5, 6-7 (rostoucí číslování)
  - Potřebují rotaci **+90°** ↻
  
- **Zadní strany**: 40-39, 38-37, 36-35 (klesající číslování)
  - Potřebují rotaci **-90°** ↺

### ✅ Výhody Tohoto Přístupu

1. **Univerzální**: Funguje pro **jakékoli pořadí stránek**
2. **Automatický**: Žádná manuální konfigurace
3. **Spolehlivý**: Založeno na matematickém pravidle
4. **Flexibilní**: Správně rotuje i nestandardní páry

---

## 🧪 Testování

Pro ověření logiky spusťte:

```bash
python test_new_rotation_logic.py
```

**Výstup ukáže:**
- ✅ Detekci lichých/sudých stránek
- ✅ Porovnání lichá vs sudá
- ✅ Určenou rotaci
- ✅ Ověření správnosti

---

## 📝 Poznámky

### ⚠️ Důležité

- Rotace se určuje **vždy podle vztahu lichá vs sudá**, ne podle pořadí v páru
- I když má pár pořadí 40-39 (klesající), logika správně určí rotaci podle toho, že 39 < 40
- Aplikace **nikdy neuplatní špatnou rotaci**, protože pravidlo je jednoznačné

### 🎯 Příklady z Praxe

**Scénář A: Tisk přední části novin**
```
Máte strany: 2, 3, 4, 5, 6, 7

Automatické párování:
  2 + 3 → Lichá (3) > Sudá (2) → +90° ↻
  4 + 5 → Lichá (5) > Sudá (4) → +90° ↻
  6 + 7 → Lichá (7) > Sudá (6) → +90° ↻
```

**Scénář B: Tisk zadní části novin**
```
Máte strany: 40, 39, 38, 37, 36, 35

Manuální párování:
  40 + 39 → Lichá (39) < Sudá (40) → -90° ↺
  38 + 37 → Lichá (37) < Sudá (38) → -90° ↺
  36 + 35 → Lichá (35) < Sudá (36) → -90° ↺
```

---

## 🔗 Související Dokumentace

- **STRÁNKY_INFO.md** - Detekce čísel stránek z názvů
- **PARSOVÁNÍ_NÁZVU.md** - Vizuální diagram parsování
- **README.md** - Kompletní dokumentace aplikace

---

**Autor:** David Rynes  
**Verze:** 2.1  
**Datum:** Říjen 2025  
**Poslední aktualizace:** Oprava logiky rotace

