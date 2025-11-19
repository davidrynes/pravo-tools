"""
PyPDF-based PDF Merger - Zachovává native CMYK barvy
"""
import logging
from pathlib import Path
from pypdf import PdfWriter, PdfReader, Transformation, PageObject
from pypdf.generic import RectangleObject

logger = logging.getLogger(__name__)

def merge_pdfs_side_by_side(left_pdf: Path, right_pdf: Path, output_path: Path, rotation: int = -90) -> bool:
    """
    Merguje dvě PDF stránky vedle sebe pomocí pypdf
    Zachovává native CMYK color space
    
    Args:
        left_pdf: Cesta k levému PDF
        right_pdf: Cesta k pravému PDF
        output_path: Cesta pro výstupní PDF
        rotation: Rotace stránky (-90 nebo +90 stupňů)
    
    Returns:
        True pokud úspěšné, False jinak
    """
    try:
        logger.info(f"🔄 PyPDF merge: {left_pdf.name} + {right_pdf.name}")
        
        # Načtení PDF souborů
        left_reader = PdfReader(str(left_pdf))
        right_reader = PdfReader(str(right_pdf))
        
        left_page = left_reader.pages[0]
        right_page = right_reader.pages[0]
        
        # Získání rozměrů
        left_box = left_page.mediabox
        right_box = right_page.mediabox
        
        left_width = float(left_box.width)
        left_height = float(left_box.height)
        right_width = float(right_box.width)
        right_height = float(right_box.height)
        
        # Vytvoření nové stránky s dvojnásobnou šířkou
        new_width = left_width + right_width
        new_height = max(left_height, right_height)
        
        # Vytvoření nové stránky
        new_page = PageObject.create_blank_page(width=new_width, height=new_height)
        
        # KLÍČOVÉ: Použijeme merge_page() s explicitní transformací
        # To zachová resources a color spaces
        
        # Přidáme levou stránku (bez transformace)
        new_page.merge_page(left_page, expand=False)
        
        # Přidáme pravou stránku s posunem doprava
        # merge_page() umí vzít Transformation jako druhý parametr
        # Ale musíme použít merge_transformed_page() nebo jiný přístup
        
        # Zkusíme merge_transformed_page() pokud existuje
        try:
            # PyPDF 3.x+ má merge_transformed_page()
            translation = Transformation().translate(tx=left_width, ty=0)
            new_page.merge_transformed_page(right_page, translation, expand=False)
        except AttributeError:
            # Fallback - použijeme CTM (Current Transformation Matrix)
            # Musíme upravit content stream
            from pypdf.generic import ContentStream, ArrayObject, NameObject
            
            # Přidáme translační matici do content streamu pravé stránky
            # PDF příkaz: q 1 0 0 1 tx ty cm (content) Q
            right_content = right_page.get_contents()
            
            if right_content:
                # Upravíme content s translací
                modified_content = (
                    f"q 1 0 0 1 {left_width} 0 cm\n".encode('latin-1') +
                    right_content.get_data() +
                    b"\nQ\n"
                )
                
                # Vytvoříme nový stream
                from pypdf.generic import StreamObject
                new_stream = StreamObject()
                new_stream._data = modified_content
                
                # Přidáme do new_page content
                if new_page.get_contents():
                    new_page[NameObject("/Contents")].append(new_stream)
                else:
                    new_page[NameObject("/Contents")] = ArrayObject([new_stream])
            
            # Merge resources z pravé stránky
            new_page.merge_page(right_page, over=True, expand=False)
        
        logger.info(f"  ✅ Stránky sloučeny pomocí merge_page()")
        
        # Aplikace rotace na celou stránku
        new_page.rotate(rotation)
        logger.info(f"  🔄 Stránka otočena o {rotation} stupňů")
        
        # Vytvoření output PDF
        writer = PdfWriter()
        writer.add_page(new_page)
        
        # Zkopírujeme metadata z levého PDF
        if left_reader.metadata:
            for key, value in left_reader.metadata.items():
                writer.add_metadata({key: value})
        
        # KLÍČOVÉ: Zkopírujeme OutputIntent z původního PDF (jednodušší a spolehlivější)
        try:
            from pypdf.generic import NameObject
            
            # Zkusíme zkopírovat OutputIntent přímo z původního PDF
            root = left_reader.trailer.get('/Root')
            if root and '/OutputIntents' in root:
                output_intents = root['/OutputIntents']
                
                # Zkopírujeme OutputIntents do writer
                catalog = writer._root_object
                catalog[NameObject("/OutputIntents")] = output_intents
                
                logger.info(f"  ✅ OutputIntent zkopírován z původního PDF")
            else:
                logger.info(f"  ℹ️  Původní PDF nemá OutputIntent v Root")
        except Exception as oi_error:
            logger.warning(f"  ⚠️  OutputIntent copy error: {oi_error}")
        
        # Uložení
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"✅ PyPDF merge úspěšný: {output_path.name}")
        return True
        
    except Exception as e:
        logger.error(f"❌ PyPDF merge error: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"  Traceback: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    # Test
    from pathlib import Path
    
    left = Path('files/PR25103038VY1.pdf')
    right = Path('files/PR25103003VY1.pdf')
    output = Path('output/test_pypdf_merge.pdf')
    
    logging.basicConfig(level=logging.INFO)
    
    success = merge_pdfs_side_by_side(left, right, output, -90)
    
    if success and output.exists():
        print(f'\n✅ Test úspěšný: {output}')
        print(f'   Velikost: {output.stat().st_size / (1024*1024):.2f} MB')
        print('\n📊 Prosím porovnejte barvy s původním PDF!')
    else:
        print('\n❌ Test selhal')

