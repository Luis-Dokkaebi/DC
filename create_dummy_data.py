import os
from PIL import Image, ImageDraw

def create_dummy_images():
    os.makedirs('Datos', exist_ok=True)
    classes = ['Zapata_Frente', 'Columna_A', 'Losa_Nivel1']
    for i in range(5):
        for cls in classes:
            img = Image.new('RGB', (200, 200), color=(i*40, 100, 100))
            d = ImageDraw.Draw(img)
            d.text((10,10), f"{cls}_{i}", fill=(255,255,255))
            img.save(f"Datos/{cls}_{i}.jpg")
    print("Dummy images created in Datos/")

if __name__ == "__main__":
    create_dummy_images()
