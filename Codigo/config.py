import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths importantes (actualizados con tu nueva estructura)
IMAGENES_DIR = os.path.join(BASE_DIR, 'Imagenes')
CODIGO_DIR = os.path.join(BASE_DIR, 'Codigo')
UTILS_DIR = os.path.join(CODIGO_DIR, 'utils')
MODELOS_DIR = os.path.join(BASE_DIR, 'Modelos')
RESULTADOS_DIR = os.path.join(BASE_DIR, 'Resultados')
DATOS_DIR = os.path.join(BASE_DIR, 'Datos')

# Parámetros de entrenamiento
BATCH_SIZE = 32
IMAGE_SIZE = (128, 128)  # Puedes ajustarlo según tu dataset
EPOCHS = 10
LEARNING_RATE = 0.001
NUM_CLASSES = 2  # Lo puedes actualizar según tu dataset

# Semilla para reproducibilidad
SEED = 42

# Configuración de Etapas de Construcción (Nombre de Clase: {Orden, Avance %})
ETAPAS = {
    "Limpieza": {"orden": 1, "avance": 10},
    "Excavacion": {"orden": 2, "avance": 20},
    "Zapata": {"orden": 3, "avance": 30},
    "Cimentacion": {"orden": 3, "avance": 30},
    "Columna": {"orden": 4, "avance": 45},
    "Muro": {"orden": 5, "avance": 60},
    "Losa": {"orden": 6, "avance": 75},
    "Instalaciones": {"orden": 7, "avance": 85},
    "Acabados": {"orden": 8, "avance": 95},
    "Entrega": {"orden": 9, "avance": 100}
}
