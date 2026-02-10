import argparse
import os
import sys

# Agregar el directorio raíz al path para poder importar Codigo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Codigo.utils.pdf_helper import extraer_imagenes_de_pdf
from Codigo import config

def main():
    parser = argparse.ArgumentParser(description="Extraer imágenes de un PDF para entrenamiento.")
    parser.add_argument("--pdf", required=True, help="Ruta al archivo PDF.")
    parser.add_argument("--clase", required=True, help="Nombre de la clase (etiqueta) para las imágenes.")

    args = parser.parse_args()

    pdf_path = args.pdf
    clase = args.clase

    if not os.path.exists(pdf_path):
        print(f"❌ Error: El archivo {pdf_path} no existe.")
        return

    # Definir directorio de salida
    output_dir = os.path.join(config.IMAGENES_DIR, clase)

    print(f"📂 Extrayendo imágenes de {pdf_path} a {output_dir}...")

    imagenes = extraer_imagenes_de_pdf(pdf_path, output_dir)

    if imagenes:
        print(f"✅ Proceso completado. {len(imagenes)} imágenes listas en {output_dir}.")
    else:
        print("⚠️ No se encontraron imágenes o hubo un error.")

if __name__ == "__main__":
    main()
