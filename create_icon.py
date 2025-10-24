#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Merger - Vytvoření ikony pro aplikaci
Autor: David Rynes
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Vytvoří ikonu pro aplikaci"""
    # Vytvoření obrázku 512x512
    size = 512
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Pozadí - modrý gradient
    for y in range(size):
        color = int(50 + (y / size) * 100)  # 50-150
        draw.rectangle([0, y, size, y+1], fill=(color, color+50, color+100, 255))
    
    # Bílý kruh
    margin = 50
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=(255, 255, 255, 200), outline=(200, 200, 200, 255), width=5)
    
    # Text "PDF"
    try:
        # Pokus o načtení fontu
        font_size = 120
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        # Fallback font
        font = ImageFont.load_default()
    
    text = "PDF"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 20
    
    draw.text((x, y), text, fill=(50, 100, 200, 255), font=font)
    
    # Text "Merger" pod PDF
    try:
        font_size = 60
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "Merger"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    x = (size - text_width) // 2
    y = y + text_height + 10
    
    draw.text((x, y), text, fill=(50, 100, 200, 255), font=font)
    
    # Uložení ikony
    img.save('icon.png')
    print("Ikona vytvořena: icon.png")
    
    # Vytvoření ikony pro macOS (.icns)
    try:
        # Pokus o vytvoření .icns souboru
        sizes = [16, 32, 64, 128, 256, 512, 1024]
        icons = []
        
        for s in sizes:
            resized = img.resize((s, s), Image.Resampling.LANCZOS)
            icons.append(resized)
        
        # Uložení jako .icns (zjednodušené - pouze PNG)
        icons[0].save('icon.icns', format='PNG')
        print("Ikona pro macOS vytvořena: icon.icns")
        
    except Exception as e:
        print(f"Chyba při vytváření .icns: {e}")
        print("Používám PNG ikonu")

if __name__ == "__main__":
    create_icon()
