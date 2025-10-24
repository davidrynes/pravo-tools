#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Merger GUI - Grafické rozhraní pro spojování PDF souborů
Autor: David Rynes
Popis: GUI aplikace pro spojování PDF souborů do dvoustrany s drag & drop podporou
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import threading
import logging
from datetime import datetime

# Import naší PDF merger třídy
try:
    from indesign_like_pdf_merger import InDesignLikePDFMerger
except ImportError:
    print("Chyba: Nelze importovat InDesignLikePDFMerger")
    sys.exit(1)

# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PDFMergerGUI:
    """GUI aplikace pro spojování PDF souborů"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger - InDesign-like spojování PDF souborů do dvoustrany")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Proměnné
        self.pdf_files = []
        self.paired_files = []
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Vytvoření GUI
        self.create_widgets()
        self.setup_drag_drop()
        
        # Automatické načtení souborů ze složky files
        self.load_files_from_directory()
        
    def create_widgets(self):
        """Vytvoří všechny GUI komponenty"""
        
        # Hlavní frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfigurace grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Nadpis
        title_label = ttk.Label(main_frame, text="PDF Merger", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sekce 1: Nahrávání souborů
        upload_frame = ttk.LabelFrame(main_frame, text="1. Nahrání PDF souborů", padding="10")
        upload_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        upload_frame.columnconfigure(2, weight=1)
        
        ttk.Button(upload_frame, text="Vybrat PDF soubory", 
                  command=self.select_files).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(upload_frame, text="Načíst ze složky files", 
                  command=self.load_files_from_directory).grid(row=0, column=1, padx=(0, 10))
        
        self.file_count_label = ttk.Label(upload_frame, text="Žádné soubory nebyly vybrány")
        self.file_count_label.grid(row=0, column=2, sticky=tk.W)
        
        # Drag & Drop oblast
        self.drop_frame = tk.Frame(upload_frame, bg="#f0f0f0", relief="ridge", bd=2)
        self.drop_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        self.drop_frame.columnconfigure(0, weight=1)
        
        drop_label = ttk.Label(self.drop_frame, text="Přetáhněte PDF soubory sem", 
                              font=("Arial", 12), background="#f0f0f0")
        drop_label.grid(row=0, column=0, pady=20)
        
        # Sekce 2: Seřazování do dvojic
        pairing_frame = ttk.LabelFrame(main_frame, text="2. Seřazování do dvojic", padding="10")
        pairing_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        pairing_frame.columnconfigure(0, weight=1)
        pairing_frame.rowconfigure(1, weight=1)
        
        # Tlačítka pro seřazování
        button_frame = ttk.Frame(pairing_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(button_frame, text="Automatické párování", 
                  command=self.auto_pair).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Vyčistit párování", 
                  command=self.clear_pairs).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Přidat pár ručně", 
                  command=self.add_manual_pair).grid(row=0, column=2)
        
        # Treeview pro zobrazení párů
        columns = ("left", "right", "output")
        self.pairs_tree = ttk.Treeview(pairing_frame, columns=columns, show="headings", height=8)
        
        self.pairs_tree.heading("left", text="Levá stránka (sudé číslo)")
        self.pairs_tree.heading("right", text="Pravá stránka (liché číslo)")
        self.pairs_tree.heading("output", text="Výstupní soubor")
        
        self.pairs_tree.column("left", width=300)
        self.pairs_tree.column("right", width=300)
        self.pairs_tree.column("output", width=200)
        
        self.pairs_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar pro treeview
        pairs_scrollbar = ttk.Scrollbar(pairing_frame, orient=tk.VERTICAL, command=self.pairs_tree.yview)
        pairs_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.pairs_tree.configure(yscrollcommand=pairs_scrollbar.set)
        
        # Kontextové menu pro treeview
        self.create_context_menu()
        
        # Sekce 3: Nastavení a spuštění
        settings_frame = ttk.LabelFrame(main_frame, text="3. Nastavení a spuštění", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Rotace
        ttk.Label(settings_frame, text="Rotace:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.rotation_var = tk.StringVar(value="-90")
        rotation_combo = ttk.Combobox(settings_frame, textvariable=self.rotation_var, 
                                    values=["-90", "90"], state="readonly", width=10)
        rotation_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(settings_frame, text="stupňů").grid(row=0, column=2, sticky=tk.W)
        
        # DPI
        ttk.Label(settings_frame, text="Kvalita (DPI):").grid(row=0, column=3, sticky=tk.W, padx=(20, 10))
        self.dpi_var = tk.StringVar(value="300")
        dpi_combo = ttk.Combobox(settings_frame, textvariable=self.dpi_var, 
                               values=["150", "300", "600"], state="readonly", width=10)
        dpi_combo.grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        
        # Výstupní složka
        ttk.Label(settings_frame, text="Výstupní složka:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.output_var = tk.StringVar(value=str(self.output_dir))
        output_entry = ttk.Entry(settings_frame, textvariable=self.output_var, width=40)
        output_entry.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0), padx=(0, 10))
        
        ttk.Button(settings_frame, text="Vybrat", 
                  command=self.select_output_dir).grid(row=1, column=4, pady=(10, 0))
        
        # Tlačítko pro spuštění
        self.merge_button = ttk.Button(settings_frame, text="Sloučit PDF soubory", 
                                      command=self.start_merge, style="Accent.TButton")
        self.merge_button.grid(row=2, column=0, columnspan=5, pady=(20, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(settings_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Log výstup
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfigurace grid váhy
        main_frame.rowconfigure(4, weight=1)
        
    def setup_drag_drop(self):
        """Nastaví drag & drop funkcionalitu"""
        self.drop_frame.bind("<Button-1>", self.on_drop_frame_click)
        self.drop_frame.bind("<B1-Motion>", self.on_drag_motion)
        self.drop_frame.bind("<ButtonRelease-1>", self.on_drop_frame_release)
        
        # Bind pro drag & drop souborů
        self.root.bind("<B1-Motion>", self.on_drag_motion)
        self.root.bind("<ButtonRelease-1>", self.on_drop_files)
        
    def on_drop_frame_click(self, event):
        """Zpracuje kliknutí na drop frame"""
        self.select_files()
        
    def on_drag_motion(self, event):
        """Zpracuje pohyb myši při drag"""
        pass
        
    def on_drop_frame_release(self, event):
        """Zpracuje uvolnění myši na drop frame"""
        pass
        
    def on_drop_files(self, event):
        """Zpracuje přetažení souborů"""
        # Tato funkce bude implementována později
        pass
        
    def create_context_menu(self):
        """Vytvoří kontextové menu pro treeview"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Odstranit pár", command=self.remove_selected_pair)
        self.context_menu.add_command(label="Upravit pár", command=self.edit_selected_pair)
        
        self.pairs_tree.bind("<Button-3>", self.show_context_menu)
        
    def show_context_menu(self, event):
        """Zobrazí kontextové menu"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def log_message(self, message):
        """Přidá zprávu do logu"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
    def load_files_from_directory(self):
        """Automaticky načte PDF soubory ze složky files"""
        files_dir = Path("files")
        if files_dir.exists():
            pdf_files = list(files_dir.glob("*.pdf"))
            if pdf_files:
                self.pdf_files = [str(f) for f in pdf_files]
                self.file_count_label.config(text=f"Načteno {len(self.pdf_files)} PDF souborů ze složky files")
                self.log_message(f"Automaticky načteno {len(self.pdf_files)} PDF souborů ze složky files")
                
                # Debug: zobrazit názvy souborů
                for i, file_path in enumerate(self.pdf_files):
                    filename = Path(file_path).name
                    page_num = self.extract_page_number(filename)
                    self.log_message(f"Soubor {i+1}: {filename} (číslo stránky: {page_num})")
                
                self.auto_pair()
            else:
                self.log_message("Ve složce files nebyly nalezeny žádné PDF soubory")
        else:
            self.log_message("Složka files neexistuje")
            
    def select_files(self):
        """Vybere PDF soubory"""
        files = filedialog.askopenfilenames(
            title="Vyberte PDF soubory",
            filetypes=[("PDF soubory", "*.pdf"), ("Všechny soubory", "*.*")]
        )
        
        if files:
            self.pdf_files = list(files)
            self.file_count_label.config(text=f"Vybráno {len(self.pdf_files)} PDF souborů")
            self.log_message(f"Nahráno {len(self.pdf_files)} PDF souborů")
            
            # Debug: zobrazit názvy souborů
            for i, file_path in enumerate(self.pdf_files):
                filename = Path(file_path).name
                page_num = self.extract_page_number(filename)
                self.log_message(f"Soubor {i+1}: {filename} (číslo stránky: {page_num})")
            
            self.auto_pair()
            
    def auto_pair(self):
        """Automaticky spáruje soubory podle čísel"""
        if not self.pdf_files:
            messagebox.showwarning("Upozornění", "Nejdříve vyberte PDF soubory")
            return
            
        self.clear_pairs()
        
        # Extrahování čísel ze souborů
        file_numbers = {}
        for file_path in self.pdf_files:
            filename = Path(file_path).name
            page_num = self.extract_page_number(filename)
            if page_num is not None:
                file_numbers[page_num] = file_path
                self.log_message(f"Nalezeno číslo stránky {page_num} pro soubor {filename}")
            else:
                self.log_message(f"Nelze extrahovat číslo stránky z {filename}")
                
        self.log_message(f"Celkem nalezeno {len(file_numbers)} souborů s čísly stránek")
                
        # Spárování sudých a lichých čísel
        paired_count = 0
        for page_num in sorted(file_numbers.keys()):
            if page_num % 2 == 0:  # Sudé číslo
                left_file = file_numbers[page_num]
                right_page_num = page_num + 1
                
                if right_page_num in file_numbers:
                    right_file = file_numbers[right_page_num]
                    output_name = f"merged_{page_num:02d}_{right_page_num:02d}.pdf"
                    
                    self.add_pair_to_tree(left_file, right_file, output_name)
                    paired_count += 1
                    self.log_message(f"Spárováno: {Path(left_file).name} + {Path(right_file).name}")
                else:
                    self.log_message(f"Nenalezena pravá stránka pro stránku {page_num}")
                    
        self.log_message(f"Automaticky spárováno {paired_count} dvojic")
        
    def extract_page_number(self, filename: str) -> Optional[int]:
        """Extrahuje číslo stránky z názvu souboru"""
        try:
            name = Path(filename).stem
            parts = name.split('_')
            if parts:
                last_part = parts[-1]
                if last_part.isdigit():
                    return int(last_part)
            return None
        except Exception:
            return None
            
    def clear_pairs(self):
        """Vyčistí všechny páry"""
        for item in self.pairs_tree.get_children():
            self.pairs_tree.delete(item)
            
    def add_pair_to_tree(self, left_file: str, right_file: str, output_name: str):
        """Přidá pár do treeview"""
        left_name = Path(left_file).name
        right_name = Path(right_file).name
        
        self.pairs_tree.insert("", tk.END, values=(left_name, right_name, output_name))
        
    def add_manual_pair(self):
        """Přidá pár ručně"""
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Upozornění", "Potřebujete alespoň 2 PDF soubory")
            return
            
        # Vytvoření dialogu pro výběr páru
        dialog = ManualPairDialog(self.root, self.pdf_files)
        if dialog.result:
            left_file, right_file, output_name = dialog.result
            self.add_pair_to_tree(left_file, right_file, output_name)
            self.log_message(f"Ručně přidán pár: {Path(left_file).name} + {Path(right_file).name}")
            
    def remove_selected_pair(self):
        """Odstraní vybraný pár"""
        selected = self.pairs_tree.selection()
        if selected:
            self.pairs_tree.delete(selected[0])
            
    def edit_selected_pair(self):
        """Upraví vybraný pár"""
        selected = self.pairs_tree.selection()
        if selected:
            item = self.pairs_tree.item(selected[0])
            values = item['values']
            if values:
                left_file = next((f for f in self.pdf_files if Path(f).name == values[0]), None)
                right_file = next((f for f in self.pdf_files if Path(f).name == values[1]), None)
                
                if left_file and right_file:
                    dialog = ManualPairDialog(self.root, self.pdf_files, 
                                           initial_left=left_file, initial_right=right_file,
                                           initial_output=values[2])
                    if dialog.result:
                        new_left, new_right, new_output = dialog.result
                        self.pairs_tree.item(selected[0], values=(Path(new_left).name, 
                                                                Path(new_right).name, 
                                                                new_output))
                        
    def select_output_dir(self):
        """Vybere výstupní složku"""
        directory = filedialog.askdirectory(title="Vyberte výstupní složku")
        if directory:
            self.output_var.set(directory)
            self.output_dir = Path(directory)
            
    def start_merge(self):
        """Spustí proces slučování"""
        if not self.pairs_tree.get_children():
            messagebox.showwarning("Upozornění", "Nejdříve vytvořte páry souborů")
            return
            
        # Spuštění v samostatném vlákně
        self.merge_button.config(state='disabled')
        self.progress.start()
        
        thread = threading.Thread(target=self.merge_files_thread)
        thread.daemon = True
        thread.start()
        
    def merge_files_thread(self):
        """Sloučí soubory v samostatném vlákně"""
        try:
            rotation = int(self.rotation_var.get())
            dpi = int(self.dpi_var.get())
            
            merger = InDesignLikePDFMerger()
            merger.output_dir = self.output_dir
            
            pairs = []
            for item in self.pairs_tree.get_children():
                values = self.pairs_tree.item(item)['values']
                if values:
                    left_name = values[0]
                    right_name = values[1]
                    output_name = values[2]
                    
                    left_file = next((f for f in self.pdf_files if Path(f).name == left_name), None)
                    right_file = next((f for f in self.pdf_files if Path(f).name == right_name), None)
                    
                    if left_file and right_file:
                        pairs.append((left_file, right_file, output_name))
                        
            self.log_message(f"Začínám slučování {len(pairs)} párů...")
            
            success_count = 0
            for i, (left_file, right_file, output_name) in enumerate(pairs):
                self.log_message(f"Slučuji pár {i+1}/{len(pairs)}: {Path(left_file).name} + {Path(right_file).name}")
                
                if merger.create_side_by_side_pdf_indesign_like(Path(left_file), Path(right_file), 
                                                self.output_dir / output_name, rotation):
                    success_count += 1
                    self.log_message(f"✓ Úspěšně vytvořeno: {output_name}")
                else:
                    self.log_message(f"✗ Chyba při vytváření: {output_name}")
                    
            self.log_message(f"Hotovo! Úspěšně vytvořeno {success_count}/{len(pairs)} PDF souborů")
            
            if success_count > 0:
                messagebox.showinfo("Úspěch", f"Úspěšně vytvořeno {success_count} PDF souborů ve složce:\n{self.output_dir}")
                
        except Exception as e:
            self.log_message(f"Chyba: {str(e)}")
            messagebox.showerror("Chyba", f"Došlo k chybě: {str(e)}")
            
        finally:
            # Obnovení GUI
            self.root.after(0, self.merge_complete)
            
    def merge_complete(self):
        """Dokončí proces slučování"""
        self.progress.stop()
        self.merge_button.config(state='normal')


class ManualPairDialog:
    """Dialog pro ruční přidání páru"""
    
    def __init__(self, parent, pdf_files, initial_left=None, initial_right=None, initial_output=None):
        self.result = None
        self.pdf_files = pdf_files
        
        # Vytvoření dialogu
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Přidat pár ručně")
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrování dialogu
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Levá stránka
        ttk.Label(main_frame, text="Levá stránka (sudé číslo):").pack(anchor=tk.W, pady=(0, 5))
        self.left_var = tk.StringVar(value=Path(initial_left).name if initial_left else "")
        left_combo = ttk.Combobox(main_frame, textvariable=self.left_var, 
                                values=[Path(f).name for f in pdf_files], state="readonly")
        left_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Pravá stránka
        ttk.Label(main_frame, text="Pravá stránka (liché číslo):").pack(anchor=tk.W, pady=(0, 5))
        self.right_var = tk.StringVar(value=Path(initial_right).name if initial_right else "")
        right_combo = ttk.Combobox(main_frame, textvariable=self.right_var, 
                                 values=[Path(f).name for f in pdf_files], state="readonly")
        right_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Výstupní soubor
        ttk.Label(main_frame, text="Název výstupního souboru:").pack(anchor=tk.W, pady=(0, 5))
        self.output_var = tk.StringVar(value=initial_output or "merged.pdf")
        output_entry = ttk.Entry(main_frame, textvariable=self.output_var)
        output_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Tlačítka
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Zrušit", command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Přidat", command=self.ok).pack(side=tk.RIGHT)
        
        # Čekání na uzavření dialogu
        self.dialog.wait_window()
        
    def ok(self):
        """Potvrdí dialog"""
        left_name = self.left_var.get()
        right_name = self.right_var.get()
        output_name = self.output_var.get()
        
        if not left_name or not right_name or not output_name:
            messagebox.showwarning("Upozornění", "Vyplňte všechna pole")
            return
            
        if left_name == right_name:
            messagebox.showwarning("Upozornění", "Levá a pravá stránka musí být různé")
            return
            
        # Najít plné cesty k souborům
        left_file = next((f for f in self.pdf_files if Path(f).name == left_name), None)
        right_file = next((f for f in self.pdf_files if Path(f).name == right_name), None)
        
        if not left_file or not right_file:
            messagebox.showerror("Chyba", "Nepodařilo se najít soubory")
            return
            
        self.result = (left_file, right_file, output_name)
        self.dialog.destroy()
        
    def cancel(self):
        """Zruší dialog"""
        self.dialog.destroy()


def main():
    """Hlavní funkce"""
    root = tk.Tk()
    
    # Nastavení stylu
    style = ttk.Style()
    style.theme_use('clam')
    
    # Vytvoření aplikace
    app = PDFMergerGUI(root)
    
    # Spuštění hlavní smyčky
    root.mainloop()


if __name__ == "__main__":
    main()
