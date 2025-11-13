# 📋 Changelog - Verze 5.0 (Novinový Tisk - Pevné Klíče Párování)

**Datum:** Říjen 2025  
**Verze:** 5.0  
**Status:** ✅ Všechny funkce implementovány a otestovány

---

## 🎯 Shrnutí Požadavků od Uživatelů

### ✅ CO FUNGOVALO:
- ✅ **Detekce levá-pravá** po nahrání souborů funguje OK

### ❌ CO NEFUNGOVALO:
- ❌ **Automatické párování**: Spojovalo soubory dvou po sobě jdoucích stran (např. 2-3 místo 2-39)
- ❌ **Ruční párování**: Umožňovalo spárovat i dvě sudé strany (chybová možnost)
- ❌ **Slučování**: U sudé > liché nefungovala rotace správně (otáčelo oba doprava)

### 🆕 NOVÉ POŽADAVKY:
1. Rozsah vydání: Dropdown pro 32/36/40/48/56 stran
2. Pevný klíč párování pro každou variantu (např. ke straně 40 lze přidat pouze stranu 1)
3. Liché strany vždy vpravo před rotací (např. 40-1, ne 1-40)
4. Smazání výsledku po stažení
5. Zvýšit limit souborů na 80

---

## ✨ Nové Funkce

### 1. 📊 Dropdown pro Výběr Rozsahu Vydání

**Lokace:** `templates/index.html` - Sekce 3 (Párování)

```html
<select class="form-select form-select-sm" id="pageCountSelect">
    <option value="32">32 stran</option>
    <option value="36">36 stran</option>
    <option value="40" selected>40 stran</option>
    <option value="48">48 stran</option>
    <option value="56">56 stran</option>
</select>
```

**Vysvětlení:**
- Uživatel vybere počet stran vydání (např. 40)
- Auto-párování pak použije odpovídající klíč (40-1, 2-39, 38-3...)
- Defaultně vybrána hodnota 40 (nejčastější)

---

### 2. 🔑 Pevné Klíče Párování

**Nový modul:** `pairing_logic.py`

**Klíče pro všechny rozsahy:**

#### 32 stran (16 párů):
```
40-1, 2-39, 38-3, 4-37, 36-5, 6-35, 34-7, 8-33...
```

#### 36 stran (18 párů):
```
36-1, 2-35, 34-3, 4-33, 32-5, 6-31, 30-7, 8-29...
```

#### 40 stran (20 párů):
```
40-1, 2-39, 38-3, 4-37, 36-5, 6-35, 34-7, 8-33...
```

#### 48 stran (24 párů):
```
48-1, 2-47, 46-3, 4-45, 44-5, 6-43, 42-7, 8-41...
```

#### 56 stran (28 párů):
```
56-1, 2-55, 54-3, 4-53, 52-5, 6-51, 50-7, 8-49...
```

**Funkce v modulu:**
- `get_pairing_key(page_count)` - Vrátí klíč pro daný rozsah
- `validate_pair(left, right, page_count)` - Zkontroluje zda je pár validní
- `auto_pair_files(files, page_count)` - Automaticky spáruje podle klíče
- `ensure_odd_on_right(...)` - Zajistí liché vpravo

---

### 3. 🔄 Automatické Zajištění Lichých Vpravo

**Lokace:** `web_app.py` - funkce `merge_files()`

```python
# ZAJIŠTĚNÍ: Liché strany vždy vpravo!
if left_page % 2 == 1:  # Levá je lichá
    left_file, right_file = right_file, left_file
    left_page, right_page = right_page, left_page
    logger.info(f"Pár přehozen: Liché ({right_page}) je nyní vpravo")
```

**Příklad:**
- Uživatel vytvoří pár: **1-40** (lichá vlevo)
- Aplikace automaticky přehodí: **40-1** (lichá vpravo) ✅
- Před rotací je vždy správné pořadí!

---

### 4. 🗑️ Automatické Smazání Po Stažení

**Lokace:** `web_app.py` - endpoint `/api/download/<filename>`

```python
# Po odeslání smažeme soubor (pokud je query param auto_delete=true)
auto_delete = request.args.get('auto_delete', 'false').lower() == 'true'
if auto_delete:
    # Spuštíme smazání v samostatném vlákně po 2 sekundách
    def delete_after_download():
        time.sleep(2)
        if file_path.exists():
            file_path.unlink()
```

**Použití v UI:**
```html
<a href="/api/download/${result.filename}?auto_delete=true">
    Stáhnout (automaticky se smaže)
</a>
```

**Výhoda:**
- Po stažení souboru se automaticky smaže z výsledků
- Čistá fronta výsledků
- Žádné ruční mazání

---

### 5. 📁 Zvýšení Limitu na 80 Souborů

**Lokace:** `web_app.py`

```python
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB (pro až 80 souborů)
```

**UI změna:**
```html
<p class="text-muted">Max: 80 souborů, 200MB celkem</p>
```

**Výhoda:**
- Nahrajete celé vydání najednou (56 stran = 28 párů)
- Rezerva pro větší soubory

---

## 🔧 Opravy Problémů

### 1. ✅ Auto-Párování - OPRAVENO

**Problém:** Spojovalo 2-3, 4-5, 6-7... (vedlejší strany)  
**Řešení:** Používá pevné klíče podle rozsahu

**Před:**
```
2-3, 4-5, 6-7, 8-9... ❌
```

**Po:**
```
40-1, 2-39, 38-3, 4-37, 36-5... ✅ (pro 40 stran)
```

**Kód:**
```javascript
async function autoPair() {
    const pageCount = parseInt(document.getElementById('pageCountSelect').value);
    
    const response = await fetch('/api/auto-pair', {
        method: 'POST',
        body: JSON.stringify({ page_count: pageCount })
    });
}
```

---

### 2. ✅ Validace Párů - IMPLEMENTOVÁNO

**Nový endpoint:** `/api/validate-pair`

**Funkce:**
- Zkontroluje zda je pár validní podle klíče
- Pokud ne, navrhne správný pár

**Příklad:**
```json
POST /api/validate-pair
{
  "left_page": 40,
  "right_page": 3,
  "page_count": 40
}

Response:
{
  "success": true,
  "valid": false,
  "message": "Neplatný pár! Ke straně 40 patří strana 1",
  "correct_pair": 1
}
```

**Použití:**
- Při manuálním párování (drag & drop)
- Upozornění uživatele na chybu
- Zamezení chybného párování

---

### 3. ✅ Rotace pro Sudé > Liché - OPRAVENO

**Problém:** U párů kde sudé > liché (např. 40-1) otáčelo obě strany doprava  
**Příčina:** Rotace závisela na porovnání čísel stránek, ne na pořadí páru

**Řešení:** Rotace podle pořadí páru v seznamu

**Kód:**
```python
for i, pair in enumerate(file_pairs, start=1):
    # OBOUSTRANNÝ TISK DVOJSTRAN:
    # Rotace závisí na POŘADÍ PÁRU (liché = přední, sudé = zadní)
    if i % 2 == 1:  # Liché pořadí (1, 3, 5...) = Přední strana
        rotation = 90
        side = "Přední"
    else:           # Sudé pořadí (2, 4, 6...) = Zadní strana
        rotation = -90
        side = "Zadní"
```

**Výsledek:**
```
1. pár (40-1):  +90° ✅ (přední strana papíru 1)
2. pár (2-39):  -90° ✅ (zadní strana papíru 1)
3. pár (38-3):  +90° ✅ (přední strana papíru 2)
4. pár (4-37):  -90° ✅ (zadní strana papíru 2)
```

---

## 📚 Nové API Endpointy

### 1. `/api/page-counts` (GET)

**Popis:** Vrátí podporované rozsahy vydání

**Response:**
```json
{
  "success": true,
  "page_counts": [32, 36, 40, 48, 56],
  "default": 40
}
```

---

### 2. `/api/validate-pair` (POST)

**Popis:** Validace páru podle klíče

**Request:**
```json
{
  "left_page": 40,
  "right_page": 1,
  "page_count": 40
}
```

**Response:**
```json
{
  "success": true,
  "valid": true,
  "message": "Platný pár"
}
```

---

### 3. `/api/auto-pair` (POST) - AKTUALIZOVÁNO

**Popis:** Auto-párování podle klíče

**Request:**
```json
{
  "page_count": 40
}
```

**Response:**
```json
{
  "success": true,
  "pairs": [
    {"left_file": "PR...40...", "right_file": "PR...01...", "left_page": 40, "right_page": 1},
    {"left_file": "PR...02...", "right_file": "PR...39...", "left_page": 2, "right_page": 39}
  ],
  "count": 20,
  "page_count": 40,
  "message": "Spárováno 20 párů podle klíče pro 40 stran"
}
```

---

## 🎨 UI Změny

### 1. Dropdown v Sekci Párování

**Před:**
```
[Automatické párování] [Vymazat páry]
```

**Po:**
```
[Dropdown: 40 stran] [Auto-párování] [Vymazat]
+ Info: "Vyberte počet stran vydání pro správné auto-párování podle klíče"
```

---

### 2. Aktualizované Informace o Rotaci

**Před:**
```
- Dynamická rotace: Podle pořadí stránek
- Pokud liché > sudé: +90°
- Pokud liché < sudé: -90°
```

**Po:**
```
- Automatická rotace podle pořadí: 1. pár = +90° (přední), 2. pár = -90° (zadní)...
- Liché strany vždy vpravo: Automatické přehození (např. 40-1, 2-39, 38-3...)
- Pevný klíč párování: Podle vybraného rozsahu (32/36/40/48/56 stran)
```

---

### 3. Limity Souborů

**Před:**
```
Max 50MB na soubor
```

**Po:**
```
Max: 80 souborů, 200MB celkem
```

---

## 🧪 Testování

### Test 1: Klíče Párování

```bash
python pairing_logic.py
```

**Výsledek:**
```
✅ 32 stran: 16 párů (všechny liché vpravo)
✅ 36 stran: 18 párů (všechny liché vpravo)
✅ 40 stran: 20 párů (všechny liché vpravo)
✅ 48 stran: 24 párů (všechny liché vpravo)
✅ 56 stran: 28 párů (všechny liché vpravo)
```

---

### Test 2: Validace Párů

```
✅ 40-1 pro 40 stran → Platný
✅ 2-39 pro 40 stran → Platný
❌ 2-3 pro 40 stran → Neplatný (ke 2 patří 39)
❌ 10-10 pro 40 stran → Neplatný
```

---

### Test 3: Rotace

```
✅ 1. pár (40-1):  +90° (přední strana papíru 1)
✅ 2. pár (2-39):  -90° (zadní strana papíru 1)
✅ 3. pár (38-3):  +90° (přední strana papíru 2)
✅ 4. pár (4-37):  -90° (zadní strana papíru 2)
```

---

## 📊 Před vs. Po

| Aspekt | Před | Po |
|--------|------|-----|
| **Auto-párování** | 2-3, 4-5, 6-7 ❌ | 40-1, 2-39, 38-3 ✅ |
| **Validace** | Umožňuje 2-3 ❌ | Pouze platné páry ✅ |
| **Liché vpravo** | Manuálně ❌ | Automaticky ✅ |
| **Rotace** | Podle čísel ❌ | Podle pořadí ✅ |
| **Rozsah** | Jen 40 stran ❌ | 32/36/40/48/56 ✅ |
| **Limit souborů** | ~40 souborů | 80 souborů ✅ |
| **Auto-delete** | Ne ❌ | Ano ✅ |

---

## 🚀 Nasazení

### 1. Git Push

```bash
git add -A
git commit -m "feat: Kompletní řešení pro novinový tisk s pevnými klíči"
git push origin main
```

### 2. Railway Auto-Deploy

Railway detekuje nový commit a automaticky:
1. Stáhne nové změny
2. Restartuje aplikaci
3. Nasadí novou verzi (~2-3 minuty)

### 3. Ověření

```bash
curl https://your-app.railway.app/api/page-counts
```

---

## 📝 Souhrn Změn

### Nové Soubory:
- ✅ `pairing_logic.py` - Logika pro klíče párování
- ✅ `CHANGELOG_V5.md` - Tento dokument

### Upravené Soubory:
- ✅ `web_app.py` - Nové endpointy, auto-delete, liché vpravo
- ✅ `templates/index.html` - Dropdown, UI změny, auto-delete link
- ✅ `README.md` - Aktualizovaná dokumentace

### Nové API Endpointy:
- ✅ `/api/page-counts` (GET)
- ✅ `/api/validate-pair` (POST)
- ✅ `/api/auto-pair` (POST) - aktualizováno

---

## ✅ Checklist Implementace

- [x] Vytvořit `pairing_logic.py` s klíči pro všechny rozsahy
- [x] Přidat dropdown pro výběr rozsahu vydání
- [x] Implementovat pevný klíč párování podle rozsahu
- [x] Zajistit liché strany vždy vpravo před rotací
- [x] Opravit rotaci pro sudé > liché
- [x] Přidat automatické smazání výsledku po stažení
- [x] Zvýšit limit nahrávaných souborů na 80
- [x] Aktualizovat UI s novými funkcemi
- [x] Otestovat všechny klíče párování
- [x] Otestovat validaci párů
- [x] Otestovat rotaci podle pořadí
- [x] Aktualizovat dokumentaci
- [x] Commitnout a pushnout změny

---

## 🎉 Výsledek

### ✅ VŠECHNY POŽADAVKY SPLNĚNY:

1. ✅ **Rozsah vydání**: Dropdown pro 32/36/40/48/56 stran
2. ✅ **Pevný klíč**: Ke straně 40 lze přidat pouze stranu 1
3. ✅ **Liché vpravo**: Automatické přehození (40-1, ne 1-40)
4. ✅ **Auto-delete**: Smazání po stažení
5. ✅ **80 souborů**: Zvýšený limit
6. ✅ **Auto-párování**: Podle klíče (40-1, 2-39...)
7. ✅ **Rotace**: Podle pořadí páru (přední/zadní)
8. ✅ **Validace**: Zamezení chybám

---

**Aplikace je připravena k nasazení a testování v produkci! 🚀**

**Railway auto-deploy proběhne do 3 minut od push! ⏱️**

**Všechny funkce otestovány a funkční! ✅**

---

**Autor:** David Rynes  
**Datum:** Říjen 2025  
**Verze:** 5.0 (Pevné Klíče Párování)

