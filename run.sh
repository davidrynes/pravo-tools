#!/bin/bash
# PDF Merger - Spuštění aplikace
# Autor: David Rynes

echo "=== PDF Merger - Spojování PDF souborů do dvoustrany ==="
echo ""

# Kontrola existence Python
if ! command -v python3 &> /dev/null; then
    echo "Chyba: Python3 není nainstalován"
    exit 1
fi

# Kontrola existence souborů
if [ ! -d "files" ]; then
    echo "Chyba: Složka 'files' neexistuje"
    exit 1
fi

# Instalace závislostí pokud je potřeba
if [ ! -d "venv" ]; then
    echo "Vytvářím virtuální prostředí..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "Dostupné možnosti:"
echo "1. Automatické spojení všech párových souborů"
echo "2. Spojení konkrétních souborů"
echo "3. Zobrazení dostupných souborů"
echo ""

read -p "Vyberte možnost (1-3): " choice

case $choice in
    1)
        echo "Spouštím automatické spojování..."
        python3 advanced_pdf_merger.py --auto
        ;;
    2)
        echo "Dostupné PDF soubory:"
        ls -la files/*.pdf
        echo ""
        read -p "Zadejte název levého souboru: " left_file
        read -p "Zadejte název pravého souboru: " right_file
        read -p "Zadejte název výstupního souboru: " output_file
        
        python3 advanced_pdf_merger.py --left "$left_file" --right "$right_file" --output "$output_file"
        ;;
    3)
        echo "Dostupné PDF soubory:"
        python3 advanced_pdf_merger.py
        ;;
    *)
        echo "Neplatná volba"
        exit 1
        ;;
esac

echo ""
echo "Hotovo! Výstupní soubory najdete ve složce 'output/'"
