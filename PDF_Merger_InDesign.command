#!/bin/bash
# PDF Merger - InDesign-like verze
# Autor: David Rynes
# Popis: Spouštěcí script pro InDesign-like PDF Merger GUI

echo "=== PDF Merger - InDesign-like verze ==="
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

# Spuštění InDesign-like GUI aplikace
echo "🚀 Spouštím InDesign-like PDF Merger GUI..."
python pdf_merger_gui.py

# Pokud se aplikace ukončí, počkat na stisk Enter
echo ""
echo "Aplikace byla ukončena."
read -p "Stiskněte Enter pro zavření okna..."
