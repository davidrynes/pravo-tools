#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Merger GUI - macOS App Bundle Launcher
Autor: David Rynes
Popis: Spouští GUI aplikaci s automatickou instalací závislostí
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

def check_dependencies():
    """Zkontroluje a nainstaluje závislosti"""
    try:
        import PyPDF2
        import reportlab
        import PIL
        import fitz
        return True
    except ImportError as e:
        return False

def install_dependencies():
    """Nainstaluje závislosti"""
    try:
        # Najít requirements.txt
        script_dir = Path(__file__).parent
        requirements_file = script_dir / "requirements.txt"
        
        if requirements_file.exists():
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
            return True
        else:
            # Instalace jednotlivých balíčků
            packages = ["PyPDF2>=3.0.0", "reportlab>=4.0.0", "Pillow>=9.0.0", "PyMuPDF>=1.23.0"]
            for package in packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Hlavní funkce"""
    # Zkontrolovat závislosti
    if not check_dependencies():
        # Zobrazit dialog pro instalaci
        root = tk.Tk()
        root.withdraw()  # Skrýt hlavní okno
        
        result = messagebox.askyesno(
            "PDF Merger - Instalace závislostí",
            "Aplikace potřebuje nainstalovat několik Python balíčků.\n\n"
            "Chcete pokračovat s automatickou instalací?\n\n"
            "Budou nainstalovány: PyPDF2, reportlab, Pillow, PyMuPDF"
        )
        
        if result:
            try:
                messagebox.showinfo("PDF Merger", "Instaluji závislosti...\n\nProsím čekejte.")
                if install_dependencies():
                    messagebox.showinfo("PDF Merger", "Závislosti úspěšně nainstalovány!\n\nSpouštím aplikaci...")
                else:
                    messagebox.showerror("PDF Merger", "Chyba při instalaci závislostí.\n\nZkuste spustit aplikaci znovu.")
                    return
            except Exception as e:
                messagebox.showerror("PDF Merger", f"Chyba při instalaci:\n{str(e)}")
                return
        else:
            messagebox.showinfo("PDF Merger", "Instalace zrušena.\n\nAplikace bude ukončena.")
            return
        
        root.destroy()
    
    # Spustit hlavní GUI aplikaci
    try:
        script_dir = Path(__file__).parent
        gui_script = script_dir / "pdf_merger_gui.py"
        
        if gui_script.exists():
            # Změnit pracovní adresář na složku se skriptem
            os.chdir(script_dir)
            
            # Importovat a spustit GUI
            sys.path.insert(0, str(script_dir))
            from pdf_merger_gui import main as gui_main
            gui_main()
        else:
            messagebox.showerror("PDF Merger", f"Nenalezen soubor: {gui_script}")
    except Exception as e:
        messagebox.showerror("PDF Merger", f"Chyba při spouštění aplikace:\n{str(e)}")

if __name__ == "__main__":
    main()