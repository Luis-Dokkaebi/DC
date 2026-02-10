# Codigo/generar_reporte.py

import os

# Solución para error "OMP: Error #15: Initializing libomp.dll..."
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
from docx import Document
from docx.shared import Inches
from Codigo import config
from Codigo.modelo_cnn import CNNBasica
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

# Cargar modelo entrenado
def cargar_modelo(ruta_modelo, num_clases):
    modelo = CNNBasica(num_classes=num_clases)
    modelo.load_state_dict(torch.load(ruta_modelo, map_location=torch.device('cpu')))
    modelo.eval()
    return modelo

# Clasificar imágenes de "Datos/"
def clasificar_imagenes(modelo, transform, clases):
    resultados = []
    for nombre_archivo in os.listdir('Datos'):
        if nombre_archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            ruta = os.path.join('Datos', nombre_archivo)
            try:
                img = Image.open(ruta).convert('RGB')
                entrada = transform(img).unsqueeze(0)
                salida = modelo(entrada)
                _, pred = torch.max(salida, 1)
                etiqueta = clases[pred.item()]
                resultados.append((nombre_archivo, etiqueta, ruta))
            except Exception as e:
                print(f"⚠️ Error con {nombre_archivo}: {e}")
    return resultados

# Graficar conteo de clases
def guardar_grafica_conteo(conteo, ruta):
    clases = list(conteo.keys())
    cantidades = list(conteo.values())

    plt.figure(figsize=(8, 5))
    plt.bar(clases, cantidades, color='skyblue')
    plt.xlabel('Clase')
    plt.ylabel('Cantidad')
    plt.title('Distribución de predicciones')
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()

# Crear documento Word
def generar_word(resultados, conteo):
    doc = Document()
    doc.add_heading('Reporte de Clasificación - Word', level=1)

    total = sum(conteo.values())
    doc.add_paragraph(f'Total de imágenes clasificadas: {total}')

    tabla = doc.add_table(rows=1, cols=2)
    tabla.style = 'Table Grid'
    tabla.cell(0, 0).text = 'Clase'
    tabla.cell(0, 1).text = 'Cantidad'

    for clase, cant in conteo.items():
        row = tabla.add_row()
        row.cells[0].text = clase
        row.cells[1].text = str(cant)

    doc.add_picture(os.path.join(config.RESULTADOS_DIR, "grafica_conteo.png"), width=Inches(5))
    doc.add_page_break()

    for nombre, etiqueta, ruta in resultados:
        doc.add_paragraph(f'{nombre} → Clase: {etiqueta}')
        img = Image.open(ruta)
        marcada_path = os.path.join(config.RESULTADOS_DIR, f"marcada_{nombre}")
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), etiqueta, fill=(255, 0, 0), font=ImageFont.load_default())
        img.save(marcada_path)
        doc.add_picture(marcada_path, width=Inches(3.5))

    output_path = os.path.join(config.RESULTADOS_DIR, 'reporte_resultados.docx')
    doc.save(output_path)
    print(f"📝 Word guardado: {output_path}")

# Crear PDF con resultados
def generar_pdf(resultados, conteo):
    pdf_path = os.path.join(config.RESULTADOS_DIR, "reporte_resultados.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Reporte de Clasificación - PDF")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Total imágenes: {sum(conteo.values())}")

    y = height - 110
    for clase, cant in conteo.items():
        c.drawString(60, y, f"{clase}: {cant}")
        y -= 20

    c.drawImage(os.path.join(config.RESULTADOS_DIR, "grafica_conteo.png"), 50, y - 250, width=500, preserveAspectRatio=True, mask='auto')
    c.showPage()

    for nombre, etiqueta, ruta in resultados:
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 50, f"{nombre} → {etiqueta}")
        marcada_path = os.path.join(config.RESULTADOS_DIR, f"marcada_{nombre}")
        if os.path.exists(marcada_path):
            c.drawImage(ImageReader(marcada_path), 50, height - 350, width=300, preserveAspectRatio=True, mask='auto')
        c.showPage()

    c.save()
    print(f"📄 PDF guardado: {pdf_path}")

# MAIN
if __name__ == "__main__":
    os.makedirs(config.RESULTADOS_DIR, exist_ok=True)

    transform = transforms.Compose([
        transforms.Resize(config.IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])

    modelo = cargar_modelo(os.path.join(config.MODELOS_DIR, 'modelo_cnn.pth'), config.NUM_CLASSES)
    clases = sorted(os.listdir(config.IMAGENES_DIR))  # nombres de carpetas = clases

    resultados = clasificar_imagenes(modelo, transform, clases)
    conteo = Counter([etq for _, etq, _ in resultados])

    guardar_grafica_conteo(conteo, os.path.join(config.RESULTADOS_DIR, "grafica_conteo.png"))
    generar_word(resultados, conteo)
    generar_pdf(resultados, conteo)
