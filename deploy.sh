#!/bin/bash

# PDF Merger - Deployment Helper Script
# Tento skript pomáhá s přípravou aplikace pro deployment

echo "🚀 PDF Merger - Deployment Helper"
echo "=================================="
echo ""

# Kontrola Git repozitáře
if [ ! -d ".git" ]; then
    echo "📦 Inicializuji Git repozitář..."
    git init
    echo "✅ Git inicializován"
else
    echo "✅ Git repozitář již existuje"
fi

# Přidání všech souborů
echo ""
echo "📝 Připravuji soubory pro commit..."
git add .

# Status
echo ""
echo "📊 Git status:"
git status --short

# Nabídka commitnutí
echo ""
read -p "❓ Chcete commitnout změny? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "💬 Commit zpráva: " commit_msg
    git commit -m "$commit_msg"
    echo "✅ Změny commitnuty"
else
    echo "⏭️  Přeskakuji commit"
fi

# Nabídka platformy
echo ""
echo "🎯 Vyberte platformu pro deployment:"
echo "1) Railway.app (doporučeno)"
echo "2) Render.com"
echo "3) Fly.io"
echo "4) Manuální - jen zobrazit instrukce"
echo ""
read -p "Volba (1-4): " -n 1 -r platform
echo ""

case $platform in
    1)
        echo ""
        echo "🚂 Railway.app Deployment"
        echo "========================"
        echo ""
        echo "📋 Kroky:"
        echo "1. Jděte na: https://railway.app"
        echo "2. Přihlaste se pomocí GitHub účtu"
        echo "3. Klikněte 'New Project' → 'Deploy from GitHub repo'"
        echo "4. Vyberte tento repozitář"
        echo "5. Railway automaticky detekuje Python aplikaci"
        echo "6. Počkejte na deployment"
        echo ""
        echo "💡 Tip: Railway poskytuje FREE tier s 500 hodinami/měsíc"
        echo ""
        read -p "❓ Chcete otevřít Railway.app? (y/n): " -n 1 -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open "https://railway.app"
        fi
        ;;
    2)
        echo ""
        echo "🎨 Render.com Deployment"
        echo "======================="
        echo ""
        echo "📋 Kroky:"
        echo "1. Jděte na: https://render.com"
        echo "2. Přihlaste se pomocí GitHub účtu"
        echo "3. Klikněte 'New +' → 'Web Service'"
        echo "4. Připojte GitHub repozitář"
        echo "5. Nastavení:"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: python web_app.py"
        echo "6. Klikněte 'Create Web Service'"
        echo ""
        echo "💡 Tip: Render FREE tier uspává aplikaci po 15 min neaktivity"
        echo ""
        read -p "❓ Chcete otevřít Render.com? (y/n): " -n 1 -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open "https://render.com"
        fi
        ;;
    3)
        echo ""
        echo "✈️  Fly.io Deployment"
        echo "===================="
        echo ""
        echo "📋 Kroky:"
        echo "1. Nainstalujte Fly CLI:"
        echo "   curl -L https://fly.io/install.sh | sh"
        echo ""
        echo "2. Přidejte do PATH:"
        echo "   export FLYCTL_INSTALL=\"/Users/\$(whoami)/.fly\""
        echo "   export PATH=\"\$FLYCTL_INSTALL/bin:\$PATH\""
        echo ""
        echo "3. Přihlaste se:"
        echo "   flyctl auth login"
        echo ""
        echo "4. Deploy:"
        echo "   flyctl launch"
        echo "   flyctl deploy"
        echo ""
        read -p "❓ Chcete spustit 'flyctl launch' nyní? (y/n): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if command -v flyctl &> /dev/null; then
                flyctl launch
            else
                echo "❌ Fly CLI není nainstalován"
                echo "💡 Nainstalujte pomocí: curl -L https://fly.io/install.sh | sh"
            fi
        fi
        ;;
    4)
        echo ""
        echo "📖 Manuální deployment"
        echo "====================="
        echo ""
        echo "📄 Více informací najdete v souboru: DEPLOYMENT.md"
        echo ""
        open "DEPLOYMENT.md" 2>/dev/null || cat "DEPLOYMENT.md"
        ;;
    *)
        echo "❌ Neplatná volba"
        ;;
esac

echo ""
echo "✅ Hotovo!"
echo ""
echo "📚 Pro více informací si přečtěte: DEPLOYMENT.md"
echo ""

