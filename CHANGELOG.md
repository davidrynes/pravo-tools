# 📋 Changelog

Všechny významné změny v tomto projektu jsou dokumentovány v tomto souboru.

---

## [2.0.0] - Říjen 2025

### 🎉 Hlavní funkce

#### ✨ Automatická detekce čísla stránky z názvu souboru
- **Automaticky rozpoznává** číslo stránky přímo z názvu PDF souboru
- **Podporuje formát**: `PRYYMMDDXXBBB.pdf` (extrahuje poslední 2 číslice)
- **Příklad**: `PRAVO_NEW_TEST03_FINAL_02.pdf` → Strana 02 (sudá)
- **Fallback**: `název_číslo.pdf` → extrahuje číslo za podtržítkem
- **Uživatel nemusí nic zadávat** - vše je automatické! 🚀

#### 🔧 Technické zlepšení
- Vylepšená funkce `parse_page_number()` v `web_app.py`
- Správná detekce sudých/lichých stránek v UI
- Barevné označení v prohlížeči:
  - 🔵 Modrý badge "Sudá" = Levá stránka
  - 🟢 Zelený badge "Lichá" = Pravá stránka

### 📚 Dokumentace
- ✅ Přidán `STRÁNKY_INFO.md` - podrobný popis detekce stránek
- ✅ Přidán `RAILWAY_DEPLOY.md` - kompletní deployment guide
- ✅ Aktualizován `README.md` - odkazy na nové funkce
- ✅ Přidány testovací skripty pro ověření funkcionality

### 🧪 Testování
- Vytvořen `test_page_parser.py` - test parsování názvů
- Vytvořen `test_real_files.py` - test reálných souborů
- Ověřeno na reálných souborech z produkce

### 🐛 Opravy
- **Opraveno**: Všechny soubory byly vyhodnocovány jako sudé (0 % 2 == 0)
- **Opraveno**: Číslo stránky se nyní správně detekuje z názvu
- **Opraveno**: Auto-párování nyní funguje správně

---

## [1.0.0] - Říjen 2025

### 🎉 První verze

#### 🌐 Webová aplikace
- Flask webová aplikace s moderním rozhraním
- Drag & drop podpora pro nahrávání souborů
- Real-time sledování zpracování
- Automatické párování souborů
- Manuální úprava párů pomocí drag & drop

#### 🖼️ Grafické rozhraní (GUI)
- Tkinter GUI aplikace
- Drag & drop podpora
- Automatické párování podle čísel stránek
- Kontextové menu pro správu párů
- Nastavení rotace a kvality

#### 🎨 InDesign-like kvalita
- Přímé kopírování PDF objektů bez konverze na obrázky
- Zachování textové editovatelnosti
- Vektorová kvalita pro ostrý tisk
- Optimalizace velikosti souborů (1-3 MB)

#### 🔄 Dynamická rotace
- Automatická rotace podle pořadí stránek
- +90° pro rostoucí pořadí (2-3, 14-15)
- -90° pro klesající pořadí (3-2, 15-14)
- Správná orientace pro tiskárny novin

#### 📦 Deployment
- Připraveno pro Railway.app
- Připraveno pro Vercel
- Procfile pro Heroku kompatibilitu
- Automatické deploymenty z GitHub

#### 📝 CLI verze
- `indesign_like_pdf_merger.py` - nejlepší kvalita
- `text_preserving_pdf_merger.py` - zachovává text
- `professional_pdf_merger.py` - pro tiskárny
- `optimized_pdf_merger.py` - nejmenší soubory
- `advanced_pdf_merger.py` - původní verze

---

## 🎯 Co přinese budoucnost?

### V plánu
- [ ] Podpora pro více stránek v jednom PDF
- [ ] Batch processing s více vlákny
- [ ] Export do různých formátů (TIFF, PNG, JPG)
- [ ] Náhled před spojením
- [ ] Historie zpracování
- [ ] Uložení nastavení
- [ ] Vlastní rotace pro každý pár
- [ ] API endpoint pro integraci s jinými systémy

---

**Autor:** David Rynes  
**Projekt:** pravo-tools  
**GitHub:** https://github.com/davidrynes/pravo-tools

