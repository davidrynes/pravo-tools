# 🚀 Rychlý Deployment Guide

## ⚡ Nejrychlejší způsob (Railway.app)

### 1️⃣ Připravte Git repozitář

```bash
cd /Users/david.rynes/Desktop/_DESKTOP/_CODE/DENIK_TOOLS/pdf-merge

# Spusťte deployment helper
./deploy.sh
```

### 2️⃣ Push na GitHub

```bash
# Vytvořte nový repozitář na: https://github.com/new
# Pojmenujte ho např: "pdf-merger"

# Pak přidejte remote:
git remote add origin https://github.com/VAS_USERNAME/pdf-merger.git
git branch -M main
git push -u origin main
```

### 3️⃣ Deploy na Railway

1. Jděte na **https://railway.app**
2. Přihlaste se pomocí **GitHub** účtu
3. Klikněte **"New Project"**
4. Vyberte **"Deploy from GitHub repo"**
5. Vyberte repozitář **"pdf-merger"**
6. Railway automaticky:
   - Detekuje Python aplikaci
   - Nainstaluje závislosti z `requirements.txt`
   - Spustí aplikaci pomocí `Procfile`
7. Počkejte 2-3 minuty
8. Vaše aplikace je LIVE na **https://your-app.railway.app** 🎉

---

## 🎯 Alternativní platformy

### Render.com
```bash
1. https://render.com → Přihlášení přes GitHub
2. New + → Web Service
3. Připojte GitHub repo
4. Build: pip install -r requirements.txt
5. Start: python web_app.py
6. Deploy!
```

### Fly.io
```bash
# Instalace
curl -L https://fly.io/install.sh | sh

# Deploy
flyctl auth login
flyctl launch
flyctl deploy
```

---

## 📋 Checklist před deploymentem

- ✅ `requirements.txt` - Python závislosti
- ✅ `Procfile` - Spouštěcí příkaz
- ✅ `runtime.txt` - Verze Pythonu
- ✅ `.gitignore` - Ignorované soubory
- ✅ `web_app.py` - Upravený pro produkci

Vše je **už připraveno**! Stačí jen pustit na GitHub a deploynout.

---

## 🆘 Problémy?

Přečtěte si kompletní guide: **DEPLOYMENT.md**

---

**Vytvořeno pro David Rynes • 2025**

