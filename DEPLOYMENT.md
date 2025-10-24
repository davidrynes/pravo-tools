# 🚀 Deployment Guide - PDF Merger Web App

Tento dokument popisuje, jak nasadit PDF Merger webovou aplikaci na různé cloudové platformy.

## 📋 Přehled podporovaných platforem

### ✅ Doporučené platformy:

1. **Railway.app** - ⭐ Nejjednodušší (FREE tier)
2. **Render.com** - Dobrá alternativa (FREE tier)
3. **Fly.io** - Pro pokročilé (FREE tier s omezeními)

### ❌ Nepodporované:
- **Vercel** - Nepodporuje file upload/storage v serverless prostředí
- **Netlify** - Stejný problém jako Vercel

---

## 🚂 1. Railway.app (Doporučeno)

### Proč Railway?
- ✅ Jednoduché nasazení
- ✅ FREE tier (500 hodin/měsíc)
- ✅ Automatické HTTPS
- ✅ Podporuje file storage
- ✅ GitHub integrace

### Postup:

1. **Vytvořte účet na Railway.app**
   - Jděte na https://railway.app
   - Přihlaste se pomocí GitHub účtu

2. **Připravte Git repozitář**
   ```bash
   cd /Users/david.rynes/Desktop/_DESKTOP/_CODE/DENIK_TOOLS/pdf-merge
   git init
   git add .
   git commit -m "Initial commit - PDF Merger Web App"
   ```

3. **Push na GitHub**
   ```bash
   # Vytvořte nový repozitář na GitHub
   # Pak:
   git remote add origin https://github.com/VAS_USERNAME/pdf-merger.git
   git branch -M main
   git push -u origin main
   ```

4. **Deploy na Railway**
   - Klikněte na "New Project"
   - Vyberte "Deploy from GitHub repo"
   - Vyberte váš repozitář
   - Railway automaticky detekuje Python aplikaci
   - Počkejte na build a deployment
   - Vaše aplikace bude dostupná na `https://your-app.railway.app`

5. **Nastavení proměnných prostředí (volitelné)**
   - V Railway dashboardu klikněte na váš projekt
   - Jděte do "Variables"
   - Přidejte: `PORT=8080`

---

## 🎨 2. Render.com

### Postup:

1. **Vytvořte účet na Render.com**
   - https://render.com
   - Přihlaste se pomocí GitHub

2. **Push kód na GitHub** (jako v Railway)

3. **Vytvořte Web Service**
   - Klikněte "New +"
   - Vyberte "Web Service"
   - Připojte GitHub repozitář
   - Nastavení:
     - **Name**: pdf-merger
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python web_app.py`
     - **Plan**: Free

4. **Deploy**
   - Klikněte "Create Web Service"
   - Render začne buildovat aplikaci
   - Aplikace bude dostupná na `https://pdf-merger.onrender.com`

---

## ✈️ 3. Fly.io (Pro pokročilé)

### Postup:

1. **Instalace Fly CLI**
   ```bash
   # macOS
   curl -L https://fly.io/install.sh | sh
   
   # Přidejte do PATH
   export FLYCTL_INSTALL="/Users/$(whoami)/.fly"
   export PATH="$FLYCTL_INSTALL/bin:$PATH"
   ```

2. **Přihlášení**
   ```bash
   flyctl auth login
   ```

3. **Inicializace a deploy**
   ```bash
   cd /Users/david.rynes/Desktop/_DESKTOP/_CODE/DENIK_TOOLS/pdf-merge
   flyctl launch
   # Odpovězte na otázky:
   # - App name: pdf-merger
   # - Region: Amsterdam (nebo nejbližší)
   # - Database: No
   
   flyctl deploy
   ```

4. **Otevření aplikace**
   ```bash
   flyctl open
   ```

---

## 📝 Potřebné soubory pro deployment

Všechny tyto soubory jsou již připraveny:

- ✅ `requirements.txt` - Python závislosti
- ✅ `Procfile` - Příkaz pro spuštění aplikace
- ✅ `runtime.txt` - Verze Pythonu
- ✅ `.gitignore` - Soubory k ignorování
- ✅ `web_app.py` - Upravený pro produkci

---

## 🔧 Testování před deploymentem

Před nasazením otestujte aplikaci lokálně:

```bash
cd /Users/david.rynes/Desktop/_DESKTOP/_CODE/DENIK_TOOLS/pdf-merge

# Aktivace virtuálního prostředí
source venv/bin/activate

# Instalace závislostí
pip install -r requirements.txt

# Spuštění
python web_app.py
```

Otevřete: http://localhost:8080

---

## ⚠️ Důležité poznámky

### Limity FREE tierů:

**Railway:**
- 500 hodin/měsíc (cca 21 dní)
- Automatické uspávání po neaktivitě
- 1GB RAM, 1GB disk

**Render:**
- Automatické uspávání po 15 minutách neaktivity
- První request po uspání trvá ~30 sekund
- 512MB RAM

**Fly.io:**
- 3 shared-cpu VMs
- 160GB bandwidth/měsíc

### Doporučení:
1. **Pro testování**: Railway nebo Render
2. **Pro produkci**: Railway (stabilnější) nebo vlastní server
3. **Pro vysokou zátěž**: Zvážit placený tier

---

## 🐛 Troubleshooting

### Chyba: "ModuleNotFoundError"
- Ujistěte se, že `requirements.txt` obsahuje všechny závislosti
- Zkontrolujte `Procfile`

### Aplikace nespouští
- Zkontrolujte logy: `railway logs` nebo v Render dashboardu
- Ověřte, že `PORT` proměnná je nastavena správně

### PDF soubory se neukládají
- Ujistěte se, že `uploads/` a `output/` složky existují
- Zkontrolujte logy pro chyby oprávnění

---

## 📞 Podpora

Pokud máte problémy s deploymentem:
1. Zkontrolujte logy aplikace
2. Ověřte, že všechny závislosti jsou správně nainstalovány
3. Otestujte aplikaci lokálně

---

## 📊 Monitorování

Po nasazení můžete sledovat:
- **Railway**: Dashboard s metrikami, logy
- **Render**: Dashboard s logy a metrikami
- **Fly.io**: `flyctl logs`, `flyctl status`

---

Vytvořeno: 2025

