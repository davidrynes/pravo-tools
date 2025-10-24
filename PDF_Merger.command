#!/bin/bash
# PDF Merger - Spustitelná aplikace pro macOS
# Autor: David Rynes

echo "=== PDF Merger - Spouštění aplikace ==="
echo ""

# Získat adresář kde se nachází tento skript
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Pracovní adresář: $SCRIPT_DIR"
echo ""

# Kontrola existence Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Chyba: Python3 není nainstalován"
    echo "Nainstalujte Python3 z https://python.org"
    read -p "Stiskněte Enter pro ukončení..."
    exit 1
fi

echo "✅ Python3 nalezen: $(python3 --version)"
echo ""

# Kontrola a instalace závislostí
echo "🔍 Kontroluji závislosti..."

# Vytvoření virtuálního prostředí pokud neexistuje
if [ ! -d "venv" ]; then
    echo "📦 Vytvářím virtuální prostředí..."
    python3 -m venv venv
fi

# Aktivace virtuálního prostředí
echo "🔄 Aktivuji virtuální prostředí..."
source venv/bin/activate

# Funkce pro kontrolu balíčku
check_package() {
    python -c "import $1" 2>/dev/null
}

# Kontrola jednotlivých balíčků
packages=("PyPDF2" "reportlab" "PIL" "fitz")
missing_packages=()

for package in "${packages[@]}"; do
    if check_package "$package"; then
        echo "✅ $package je nainstalován"
    else
        echo "❌ $package chybí"
        missing_packages+=("$package")
    fi
done

# Instalace chybějících balíčků
if [ ${#missing_packages[@]} -gt 0 ]; then
    echo ""
    echo "📦 Instaluji chybějící závislosti..."
    
    # Instalace všech balíčků najednou
    pip install PyPDF2>=3.0.0 reportlab>=4.0.0 Pillow>=9.0.0 PyMuPDF>=1.23.0
    
    echo ""
    echo "✅ Závislosti nainstalovány!"
fi

echo ""
echo "🚀 Spouštím PDF Merger GUI..."
echo ""

# Spuštění GUI aplikace
python pdf_merger_gui.py

# Pokud se aplikace ukončí, počkat na stisk Enter
echo ""
echo "Aplikace byla ukončena."
read -p "Stiskněte Enter pro zavření okna..."
