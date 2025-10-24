#!/bin/bash
# PDF Merger Web App - Spouštěcí script
# Autor: David Rynes
# Popis: Spouštěcí script pro webovou aplikaci PDF Merger

echo "=== PDF Merger Web App ==="
echo "Pracovní adresář: $(pwd)"

# Kontrola Python3
if command -v python3 &> /dev/null; then
    echo "✅ Python3 nalezen: $(python3 --version)"
else
    echo "❌ Python3 není nainstalován"
    exit 1
fi

# Kontrola závislostí
echo "🔍 Kontroluji závislosti..."

# Vytvoření virtuálního prostředí pokud neexistuje
if [ ! -d "venv" ]; then
    echo "📦 Vytvářím virtuální prostředí..."
    python3 -m venv venv
fi

# Aktivace virtuálního prostředí
echo "🔄 Aktivuji virtuální prostředí..."
source venv/bin/activate

# Kontrola a instalace závislostí
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Instaluji Flask..."
    pip install Flask>=2.3.0 Werkzeug>=2.3.0
else
    echo "✅ Flask je nainstalován"
fi

if ! python -c "import PyPDF2" 2>/dev/null; then
    echo "📥 Instaluji PyPDF2..."
    pip install PyPDF2>=3.0.0
else
    echo "✅ PyPDF2 je nainstalován"
fi

if ! python -c "import reportlab" 2>/dev/null; then
    echo "📥 Instaluji reportlab..."
    pip install reportlab>=4.0.0
else
    echo "✅ reportlab je nainstalován"
fi

if ! python -c "import PIL" 2>/dev/null; then
    echo "📥 Instaluji Pillow..."
    pip install Pillow>=9.0.0
else
    echo "✅ PIL je nainstalován"
fi

if ! python -c "import fitz" 2>/dev/null; then
    echo "📥 Instaluji PyMuPDF..."
    pip install PyMuPDF>=1.23.0
else
    echo "✅ fitz je nainstalován"
fi

# Vytvoření potřebných složek
echo "📁 Vytvářím potřebné složky..."
mkdir -p uploads
mkdir -p output
mkdir -p templates

# Spuštění webové aplikace
echo "🚀 Spouštím webovou aplikaci..."
echo ""
echo "🌐 Webová aplikace bude dostupná na:"
echo "   http://localhost:8080"
echo "   http://127.0.0.1:8080"
echo ""
echo "📱 Můžete použít jakýkoli prohlížeč"
echo "🔄 Pro ukončení stiskněte Ctrl+C"
echo ""

python web_app.py
