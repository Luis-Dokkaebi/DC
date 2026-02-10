import os

# Solución para error "OMP: Error #15: Initializing libomp.dll..."
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
from torchvision import transforms
from PIL import Image
import sys

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Codigo import config
from Codigo.modelo_cnn import CNNBasica

def cargar_modelo(ruta_modelo, num_clases):
    """Carga el modelo entrenado."""
    if not os.path.exists(ruta_modelo):
        print(f"❌ Error: No se encontró el modelo en {ruta_modelo}")
        return None

    modelo = CNNBasica(num_classes=num_clases)
    try:
        modelo.load_state_dict(torch.load(ruta_modelo, map_location=torch.device('cpu')))
        modelo.eval()
        print(f"✅ Modelo cargado desde {ruta_modelo}")
        return modelo
    except Exception as e:
        print(f"❌ Error al cargar modelo: {e}")
        return None

def predecir_avance(modelo, imagen_path, clases):
    """Predice la clase y devuelve el porcentaje de avance."""
    if not os.path.exists(imagen_path):
        print(f"⚠️ La imagen {imagen_path} no existe.")
        return None

    transform = transforms.Compose([
        transforms.Resize(config.IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])

    try:
        img = Image.open(imagen_path).convert('RGB')
        entrada = transform(img).unsqueeze(0)  # Añadir dimensión de batch

        with torch.no_grad():
            salida = modelo(entrada)
            _, pred = torch.max(salida, 1)

        clase_predicha = clases[pred.item()]

        # Buscar en el mapa de avance
        porcentaje = config.AVANCE_MAP.get(clase_predicha)

        if porcentaje is None:
            print(f"⚠️ La clase '{clase_predicha}' no está en el mapa de avance.")
            return None

        return clase_predicha, porcentaje

    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Uso: python Codigo/demo_avance.py <ruta_imagen_o_carpeta>")
        return

    entrada_path = sys.argv[1]

    # Obtener clases (nombres de carpetas en Imagenes/)
    if not os.path.exists(config.IMAGENES_DIR):
        print(f"❌ Error: No existe el directorio de imágenes {config.IMAGENES_DIR}")
        return

    clases = sorted(os.listdir(config.IMAGENES_DIR))

    # Cargar modelo
    modelo_path = os.path.join(config.MODELOS_DIR, 'modelo_cnn.pth')
    modelo = cargar_modelo(modelo_path, len(clases))

    if not modelo:
        return

    archivos_para_procesar = []

    if os.path.isfile(entrada_path):
        archivos_para_procesar.append(entrada_path)
    elif os.path.isdir(entrada_path):
        for f in os.listdir(entrada_path):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                archivos_para_procesar.append(os.path.join(entrada_path, f))
    else:
        print("❌ La ruta proporcionada no es válida.")
        return

    if not archivos_para_procesar:
        print("⚠️ No se encontraron imágenes para procesar.")
        return

    total_avance = 0
    conteo = 0

    print("\n📊 --- Reporte de Avance de Obra ---")

    for archivo in archivos_para_procesar:
        resultado = predecir_avance(modelo, archivo, clases)
        if resultado:
            clase, avance = resultado
            print(f"🖼️ {os.path.basename(archivo)}: {clase} -> {avance}% completado")
            total_avance += avance
            conteo += 1

    if conteo > 0:
        promedio = total_avance / conteo
        print("\n" + "="*40)
        print(f"🏗️  AVANCE PROMEDIO ESTIMADO: {promedio:.2f}%")
        print("="*40)
    else:
        print("\n❌ No se pudo calcular el avance.")

if __name__ == "__main__":
    main()
