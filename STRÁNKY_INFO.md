# 📄 Automatická Detekce Čísel Stránek

## 🎯 Jak Funguje Detekce

Aplikace **automaticky rozpoznává číslo stránky** přímo z názvu PDF souboru. Uživatel **nemusí nic zadávat** - číslo se detekuje automaticky!

---

## 📋 Podporované Formáty Názvů

### 1. **Tiskový Formát** (hlavní použití)

```
PRYYMMDDXXBBB.pdf
```

Kde:
- `PR` = Prefix (např. PRAVO, PR)
- `YYMMDD` = Datum vydání (např. 251030 = 30. října 2025)
- `XX` = **Číslo stránky** (01 až 99) - **4. a 5. znak od konce**
- `BBB` = Mutace/verze (např. VY1, 001, FINAL)

**Příklady:**
```
PR25103001VY1.pdf              →  Strana 01 (lichá)  🟢
PR25103002VY1.pdf              →  Strana 02 (sudá)   🔵
PR25103003VY1.pdf              →  Strana 03 (lichá)  🟢
PR25103040VY1.pdf              →  Strana 40 (sudá)   🔵
PRAVO_NEW_TEST03_FINAL_02.pdf  →  Strana 02 (sudá)   🔵 (fallback)
```

**Jak to funguje:**
- Aplikace extrahuje **4. a 5. znak od konce názvu** (před BBB)
- `PR25103001VY1` → znaky na pozici [-5:-3] = `01`

### 2. **Standardní Formát** (fallback)

```
název_číslo.pdf
```

**Příklady:**
```
dokument_15.pdf  →  Strana 15
test_05.pdf      →  Strana 05
```

---

## 🔄 Automatické Párování

Aplikace automaticky páruje soubory podle pravidla:

- **Sudá stránka** (2, 4, 6, ...) = **Levá stránka**
- **Lichá stránka** (3, 5, 7, ...) = **Pravá stránka**

### Příklad párování:

```
Máte soubory:
  - PRAVO_NEW_TEST03_FINAL_02.pdf (strana 2 - sudá)
  - PRAVO_NEW_TEST03_FINAL_03.pdf (strana 3 - lichá)
  - PRAVO_NEW_TEST03_FINAL_14.pdf (strana 14 - sudá)
  - PRAVO_NEW_TEST03_FINAL_15.pdf (strana 15 - lichá)

Automaticky se vytvoří páry:
  ✅ Pár 1: Strana 2 (levá) + Strana 3 (pravá)
  ✅ Pár 2: Strana 14 (levá) + Strana 15 (pravá)
```

---

## 🔄 Automatická Rotace

Aplikace **automaticky určí správnou rotaci** podle pořadí stránek:

- **Strana 2 + 3** (rostoucí) → **+90°** rotace
- **Strana 3 + 2** (klesající) → **-90°** rotace

---

## 🎨 Barevné Označení v UI

V aplikaci uvidíte:

- 🔵 **Modrý badge "Sudá"** = Levá stránka (2, 4, 6, ...)
- 🟢 **Zelený badge "Lichá"** = Pravá stránka (1, 3, 5, ...)

---

## ✅ Testování

Pro ověření správné detekce můžete spustit:

```bash
cd /Users/david.rynes/Desktop/_DESKTOP/_CODE/DENIK_TOOLS/pdf-merge
source venv/bin/activate
python test_real_files.py
```

Tento skript analyzuje všechny PDF v složce `files/` a ukáže:
- Detekované číslo stránky
- Sudá/lichá klasifikace
- Automatické párování
- Určenou rotaci

---

## 📝 Poznámky

- ✅ Aplikace **vždy preferuje** poslední 2 číslice z názvu souboru
- ✅ Pokud poslední 2 znaky nejsou číslo, zkusí se fallback (číslo za podtržítkem)
- ✅ Pokud se číslo nepodaří detekovat, vrátí se 0
- ✅ Soubory s číslem 0 se **nezobrazí** v seznamu k párování

---

## 🚀 Jak Používat

1. **Nahrajte PDF soubory** s názvem ve formátu `PRYYMMDDXXBBB.pdf`
2. Aplikace **automaticky detekuje** čísla stránek
3. Klikněte na **"Auto-párovat"** pro automatické vytvoření párů
4. Klikněte na **"Spojit PDF"** pro vytvoření výsledných souborů

**Hotovo!** 🎉

---

## 🔧 Technické Detaily

Detekce probíhá ve funkci `parse_page_number()` v souboru `web_app.py`:

```python
def parse_page_number(self, filename: str) -> int:
    name = Path(filename).stem
    
    # Primární: Extrahuje 4. a 5. znak od konce (před BBB)
    # Formát: PRYYMMDDXXBBB -> XX jsou na pozici [-5:-3]
    if len(name) >= 5:
        page_chars = name[-5:-3]
        if page_chars.isdigit():
            return int(page_chars)
    
    # Fallback 1: poslední 2 znaky
    if len(name) >= 2:
        last_two = name[-2:]
        if last_two.isdigit():
            return int(last_two)
    
    # Fallback 2: číslo za posledním podtržítkem
    parts = name.split('_')
    if parts and parts[-1].isdigit():
        return int(parts[-1])
    
    return 0
```

**Vysvětlení:**
- `name[-5:-3]` = znaky na pozici -5 a -4 (4. a 5. znak od konce)
- Pro `PR25103001VY1`: `01` (před `VY1`)
- Pro `PR25103040VY1`: `40` (před `VY1`)

---

**Autor:** David Rynes  
**Verze:** 2.0 (s automatickou detekcí)  
**Datum:** Říjen 2025

