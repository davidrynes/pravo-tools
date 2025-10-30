# 🚂 Railway Deployment Guide

## ✅ Co je připraveno

Projekt je **plně připraven** pro deployment na Railway. Všechny potřebné soubory jsou již vytvořeny:

- ✅ `Procfile` - definuje příkaz pro spuštění
- ✅ `requirements.txt` - seznam Python balíčků
- ✅ `runtime.txt` - specifikuje verzi Pythonu
- ✅ `.gitignore` - ignoruje nepotřebné soubory
- ✅ `web_app.py` - webová aplikace s Flask

---

## 🚀 Krok za krokem deployment

### 1. Otevřete Railway.app

Jděte na: **https://railway.app**

### 2. Přihlaste se pomocí GitHub

- Klikněte na **"Login"**
- Vyberte **"Login with GitHub"**
- Autorizujte Railway přístup k vašemu GitHub účtu

### 3. Vytvořte nový projekt

- Klikněte na **"New Project"**
- Vyberte **"Deploy from GitHub repo"**
- V seznamu najděte a vyberte: **`davidrynes/pravo-tools`**
- Railway automaticky začne build proces

### 4. Počkejte na deployment

Railway automaticky:
- 🔍 Detekuje Python aplikaci
- 📦 Nainstaluje závislosti z `requirements.txt`
- ▶️ Spustí aplikaci podle `Procfile`
- 🌐 Vytvoří veřejnou URL

**Build trvá cca 2-3 minuty.**

### 5. Získejte URL vaší aplikace

Po dokončení build procesu:
- Klikněte na váš projekt
- V záložce **"Settings"** najděte **"Domains"**
- Zkopírujte vygenerovanou URL (např. `https://pravo-tools-production.up.railway.app`)

### 6. Otevřete aplikaci

Otevřete URL ve vašem prohlížeči a aplikace je **LIVE!** 🎉

---

## 🔄 Automatické aktualizace

Railway je nastaveno na **automatický deployment**:

- ✅ Každý `git push` do `main` větve spustí automatický rebuild
- ✅ Aplikace se aktualizuje bez manuálního zásahu
- ✅ Můžete sledovat logy v Railway dashboardu

---

## 📊 Railway Dashboard

V Railway dashboardu můžete:

- 📈 **Metrics** - sledovat využití CPU, RAM, sítě
- 📝 **Logs** - zobrazit logy aplikace v real-time
- ⚙️ **Settings** - nastavit environment variables, custom domain
- 💰 **Usage** - sledovat využití free tieru

---

## 🆓 Free Tier Limity

Railway Free tier poskytuje:

- ✅ **500 hodin** runtime měsíčně
- ✅ **100 GB** bandwidth měsíčně
- ✅ **HTTPS** automaticky
- ✅ **Automatické deploymenty**
- ✅ **Neomezený počet projektů**

Pro tuto aplikaci je free tier **více než dostatečný**.

---

## 🔧 Řešení problémů

### Aplikace se nespouští

1. Zkontrolujte logy v Railway dashboardu
2. Ujistěte se, že všechny závislosti jsou v `requirements.txt`
3. Ověřte, že `Procfile` obsahuje správný příkaz

### Port Error

Railway automaticky nastavuje `PORT` environment variable. Aplikace ji používá:

```python
port = int(os.environ.get('PORT', 8080))
```

### Build trvá příliš dlouho

To je normální při prvním deployi. Další buildy budou rychlejší díky cache.

---

## 🌐 Vlastní doména (volitelné)

Pokud chcete použít vlastní doménu:

1. V Railway dashboardu jděte do **Settings → Domains**
2. Klikněte na **"Add Domain"**
3. Zadejte vaši doménu (např. `pdf-merger.example.com`)
4. Nastavte DNS záznamy podle instrukcí Railway
5. Railway automaticky vygeneruje SSL certifikát

---

## 📦 Co Railway dělá automaticky

```
1. Detekuje Python projekt
   ↓
2. Přečte requirements.txt
   ↓
3. Nainstaluje závislosti
   ↓
4. Přečte runtime.txt (Python 3.11)
   ↓
5. Spustí příkaz z Procfile
   ↓
6. Vytvoří veřejnou URL
   ↓
7. Aplikace je LIVE! 🎉
```

---

## 🔗 Užitečné odkazy

- **Railway Dashboard**: https://railway.app/dashboard
- **Railway Docs**: https://docs.railway.app
- **GitHub Repo**: https://github.com/davidrynes/pravo-tools
- **Support**: https://railway.app/discord

---

## ✅ Checklist

- [x] Kód je na GitHubu (`davidrynes/pravo-tools`)
- [x] Procfile je vytvořen
- [x] requirements.txt je vytvořen
- [x] runtime.txt je vytvořen
- [ ] Přihlásit se na Railway.app
- [ ] Vytvořit nový projekt
- [ ] Vybrat GitHub repo
- [ ] Počkat na deployment
- [ ] Otevřít aplikaci a otestovat

---

**Hotovo!** Vaše aplikace běží na Railway! 🚂🎉

---

**Poslední aktualizace:** Říjen 2025  
**Autor:** David Rynes

