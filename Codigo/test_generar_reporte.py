import unittest
import os
import sys
from PIL import Image

# Agrega la raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Codigo import config
from Codigo.generar_reporte_pdf import ReportePDF

class TestReportePDF(unittest.TestCase):
    def setUp(self):
        self.output_path = "test_report.pdf"
        self.config_data = config.REPORT_CONFIG
        self.dummy_image_path = "test_img.jpg"

        # Create a dummy image
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(self.dummy_image_path)

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        if os.path.exists(self.dummy_image_path):
            os.remove(self.dummy_image_path)

    def test_pdf_creation(self):
        reporte = ReportePDF(self.output_path, self.config_data)
        resultados = [("test_img.jpg", "Zapata_Frente", self.dummy_image_path)]
        conteo = {"Zapata_Frente": 1}
        etapa = "Zapata"
        porcentaje = 30

        # Test full build
        try:
            reporte.build_pdf(resultados, conteo, etapa, porcentaje)
        except Exception as e:
            self.fail(f"build_pdf failed: {e}")

        self.assertTrue(os.path.exists(self.output_path))
        self.assertGreater(os.path.getsize(self.output_path), 0)

if __name__ == '__main__':
    unittest.main()
