import unittest
import os
import shutil
import sys
from PIL import Image
from reportlab.pdfgen import canvas

# Agregar directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Codigo.utils.pdf_helper import extraer_imagenes_de_pdf

class TestPDFExtraction(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_temp"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir, exist_ok=True)

        self.pdf_path = os.path.join(self.test_dir, "test.pdf")
        self.output_dir = os.path.join(self.test_dir, "output")

        # Crear imagen temporal
        self.img_path = os.path.join(self.test_dir, "test_img.jpg")
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(self.img_path)

        # Crear PDF con la imagen
        c = canvas.Canvas(self.pdf_path)
        c.drawImage(self.img_path, 10, 10, 100, 100)
        c.save()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_extract_images(self):
        print(f"Testing extraction from {self.pdf_path} to {self.output_dir}")
        extracted = extraer_imagenes_de_pdf(self.pdf_path, self.output_dir)

        # Verificar que se extrajo al menos una imagen
        self.assertTrue(len(extracted) > 0, "No se extrajeron imágenes")

        # Verificar que el archivo existe
        self.assertTrue(os.path.exists(extracted[0]), "El archivo extraído no existe")

        # Verificar que es una imagen válida
        try:
            with Image.open(extracted[0]) as img:
                img.verify()
        except Exception as e:
            self.fail(f"La imagen extraída no es válida: {e}")

if __name__ == '__main__':
    unittest.main()
