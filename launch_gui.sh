#!/bin/bash
# PDF Merger GUI Launcher
# Autor: David Rynes

echo "=== PDF Merger GUI ==="
echo "Spouštím grafické rozhraní..."
echo ""

# Kontrola existence Python
if ! command -v python3 &> /dev/null; then
    echo "Chyba: Python3 není nainstalován"
    exit 1
fi

# Aktivace virtuálního prostředí pokud existuje
if [ -d "venv" ]; then
    echo "Aktivuji virtuální prostředí..."
    source venv/bin/activate
fi

# Spuštění GUI aplikace
python3 pdf_merger_gui.py
