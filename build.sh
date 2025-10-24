#!/bin/bash
# Build script pro PDF Merger GUI
# Autor: David Rynes

echo "=== PDF Merger GUI - Build Script ==="
echo ""

# Kontrola existence Python
if ! command -v python3 &> /dev/null; then
    echo "Chyba: Python3 není nainstalován"
    exit 1
fi

# Kontrola existence PyInstaller
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "Instaluji PyInstaller..."
    pip3 install pyinstaller
fi

# Vytvoření virtuálního prostředí pokud neexistuje
if [ ! -d "venv" ]; then
    echo "Vytvářím virtuální prostředí..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install pyinstaller
else
    source venv/bin/activate
fi

echo "Instaluji závislosti..."
pip install -r requirements.txt
pip install pyinstaller

echo ""
echo "Vytvářím spustitelný soubor..."

# Vytvoření spustitelného souboru
pyinstaller --onefile --windowed --name "PDF_Merger" \
    --add-data "advanced_pdf_merger.py:." \
    --add-data "requirements.txt:." \
    --add-data "README.md:." \
    --hidden-import "tkinter" \
    --hidden-import "tkinter.ttk" \
    --hidden-import "tkinter.filedialog" \
    --hidden-import "tkinter.messagebox" \
    --hidden-import "tkinter.scrolledtext" \
    --hidden-import "PyPDF2" \
    --hidden-import "reportlab" \
    --hidden-import "PIL" \
    --hidden-import "fitz" \
    pdf_merger_gui.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Spustitelný soubor úspěšně vytvořen!"
    echo "📁 Umístění: dist/PDF_Merger"
    echo ""
    echo "Spuštění aplikace:"
    echo "  ./dist/PDF_Merger"
    echo ""
    echo "Nebo můžete spustit GUI přímo:"
    echo "  python3 pdf_merger_gui.py"
else
    echo ""
    echo "❌ Chyba při vytváření spustitelného souboru"
    exit 1
fi
