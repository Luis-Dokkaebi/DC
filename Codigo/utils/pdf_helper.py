import os
from pypdf import PdfReader
from PIL import Image
import io

def extraer_imagenes_de_pdf(pdf_path, output_dir):
    """
    Extrae todas las imágenes de un archivo PDF y las guarda en el directorio especificado.

    Args:
        pdf_path (str): Ruta al archivo PDF.
        output_dir (str): Directorio donde guardar las imágenes extraídas.

    Returns:
        list: Lista de rutas de las imágenes extraídas.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"Error al leer el PDF {pdf_path}: {e}")
        return []

    count = 0
    extracted_paths = []

    print(f"Analizando {len(reader.pages)} páginas en {pdf_path}...")

    for i, page in enumerate(reader.pages):
        try:
            for image_file_object in page.images:
                try:
                    # Cargar datos de imagen en Pillow para verificar formato
                    image_data = io.BytesIO(image_file_object.data)
                    with Image.open(image_data) as img:
                        # Determinar extensión basada en el formato detectado por Pillow
                        ext = f".{img.format.lower()}" if img.format else ".jpg"

                        image_name = f"page_{i+1}_{count}{ext}"
                        image_path = os.path.join(output_dir, image_name)

                        img.save(image_path)
                        extracted_paths.append(image_path)
                        count += 1
                except Exception as e:
                    print(f"⚠️ Error al procesar imagen en página {i+1}: {e}")
                    continue
        except Exception as e:
            print(f"Error al procesar página {i+1}: {e}")
            continue

    print(f"✅ Se extrajeron {count} imágenes en {output_dir}")
    return extracted_paths
