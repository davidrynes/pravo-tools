@echo off
REM PDF Merger - Spustitelná aplikace pro Windows
REM Autor: David Rynes

echo === PDF Merger - Spousteni aplikace ===
echo.

REM Získat adresář kde se nachází tento skript
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Pracovni adresar: %SCRIPT_DIR%
echo.

REM Kontrola existence Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Chyba: Python neni nainstalovan
    echo Nainstalujte Python z https://python.org
    pause
    exit /b 1
)

echo ✅ Python nalezen
echo.

REM Kontrola a instalace závislostí
echo 🔍 Kontroluji zavislosti...

REM Instalace závislostí
echo 📦 Instaluji zavislosti...
python -m pip install PyPDF2>=3.0.0 reportlab>=4.0.0 Pillow>=9.0.0 PyMuPDF>=1.23.0

if errorlevel 1 (
    echo ❌ Chyba pri instalaci zavislosti
    pause
    exit /b 1
)

echo.
echo ✅ Zavislosti nainstalovany!
echo.
echo 🚀 Spoustim PDF Merger GUI...
echo.

REM Spuštění GUI aplikace
python pdf_merger_gui.py

REM Pokud se aplikace ukončí, počkat na stisk klávesy
echo.
echo Aplikace byla ukoncena.
pause
