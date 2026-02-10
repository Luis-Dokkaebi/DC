import os
import sys

# Agregar el directorio padre al sys.path para poder importar módulos hermanos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from torchvision import transforms
from PIL import Image
from Codigo.modelo_cnn import CNNBasica
from Codigo import config

# CONFIGURACIÓN DE ETAPAS Y PORCENTAJES
# Define tus etapas aquí con sus porcentajes de avance
# Asegúrate de que los nombres de las claves coincidan con los nombres de las carpetas en 'Imagenes/'
MAPA_AVANCE = {
    '0_Terreno': 0,
    '1_Cimentacion': 20,
    '2_Estructura': 40,
    '3_Techado': 60,
    '4_Obra_Negra': 80,
    '5_Acabados': 100
}

def cargar_modelo():
    """Carga el modelo entrenado."""
    modelo_path = os.path.join(config.MODELOS_DIR, 'modelo_cnn.pth')
    if not os.path.exists(modelo_path):
        print("❌ Error: No se encontró el modelo entrenado.")
        return None, None

    # Asumimos que las clases son las carpetas en 'Imagenes/' ordenadas alfabéticamente
    clases = sorted(os.listdir(config.IMAGENES_DIR))

    modelo = CNNBasica(num_classes=len(clases))
    try:
        modelo.load_state_dict(torch.load(modelo_path, map_location=torch.device('cpu')))
    except Exception as e:
        print(f"❌ Error al cargar los pesos del modelo: {e}")
        return None, None

    modelo.eval()
    return modelo, clases

def obtener_avance_por_clase(nombre_clase):
    """Obtiene el porcentaje de avance asociado a una clase."""
    # Buscar coincidencia parcial si el nombre exacto no está
    for etapa, porcentaje in MAPA_AVANCE.items():
        if etapa in nombre_clase:
            return porcentaje
    return 0  # Por defecto si no se encuentra

def main():
    print("🚧 Iniciando cálculo de avance de obra...")

    transform = transforms.Compose([
        transforms.Resize(config.IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])

    modelo, clases = cargar_modelo()
    if modelo is None:
        return

    imagenes_dir = 'Datos'
    if not os.path.exists(imagenes_dir):
        print(f"❌ La carpeta '{imagenes_dir}' no existe.")
        return

    total_avance = 0
    conteo_imagenes = 0
    detalles = []

    print(f"📂 Analizando imágenes en '{imagenes_dir}'...")

    for nombre_archivo in os.listdir(imagenes_dir):
        if nombre_archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            ruta = os.path.join(imagenes_dir, nombre_archivo)
            try:
                img = Image.open(ruta).convert('RGB')
                entrada = transform(img).unsqueeze(0)

                with torch.no_grad():
                    salida = modelo(entrada)
                    _, pred = torch.max(salida, 1)

                etiqueta = clases[pred.item()]
                avance = obtener_avance_por_clase(etiqueta)

                detalles.append(f" - {nombre_archivo}: {etiqueta} ({avance}%)")
                total_avance += avance
                conteo_imagenes += 1

            except Exception as e:
                print(f"⚠️ Error procesando {nombre_archivo}: {e}")

    if conteo_imagenes == 0:
        print("⚠️ No se encontraron imágenes válidas para analizar.")
        return

    print("\n📝 Detalles por imagen:")
    for det in detalles:
        print(det)

    promedio_avance = total_avance / conteo_imagenes
    print("\n" + "="*40)
    print(f"📊 REPORTE DE AVANCE DE OBRA")
    print("="*40)
    print(f"📷 Imágenes analizadas: {conteo_imagenes}")
    print(f"📈 Avance Promedio Estimado: {promedio_avance:.2f}%")
    print("="*40)

    print("\n💡 Nota: Este avance es un promedio basado en las fotos tomadas.")
    print("   Para mejorar la precisión, asegúrate de tomar fotos representativas de toda la obra.")

if __name__ == "__main__":
    main()
