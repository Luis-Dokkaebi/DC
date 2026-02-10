# Codigo/utils/verifica_imagenes.py

import os
from PIL import Image
from Codigo import config

def verificar_imagenes(directorio):
    errores = []
    total = 0
    buenas = 0

    for root, _, files in os.walk(directorio):
        for nombre in files:
            ruta = os.path.join(root, nombre)
            if nombre.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                total += 1
                try:
                    with Image.open(ruta) as img:
                        img.verify()  # Verifica sin cargar en memoria
                    buenas += 1
                except Exception as e:
                    errores.append((ruta, str(e)))

    print(f"📊 Total de imágenes analizadas: {total}")
    print(f"✅ Imágenes correctas: {buenas}")
    print(f"❌ Imágenes con error: {len(errores)}")

    if errores:
        print("\n🔍 Lista de imágenes dañadas o corruptas:")
        for ruta, error in errores:
            print(f" - {ruta} → {error}")

if __name__ == "__main__":
    verificar_imagenes(config.IMAGENES_DIR)
