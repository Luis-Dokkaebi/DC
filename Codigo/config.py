import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths importantes (actualizados con tu nueva estructura)
IMAGENES_DIR = os.path.join(BASE_DIR, 'Imagenes')
CODIGO_DIR = os.path.join(BASE_DIR, 'Codigo')
UTILS_DIR = os.path.join(CODIGO_DIR, 'utils')
MODELOS_DIR = os.path.join(BASE_DIR, 'Modelos')
RESULTADOS_DIR = os.path.join(BASE_DIR, 'Resultados')

# Parámetros de entrenamiento
BATCH_SIZE = 32
IMAGE_SIZE = (128, 128)  # Puedes ajustarlo según tu dataset
EPOCHS = 10
LEARNING_RATE = 0.001
NUM_CLASSES = 2  # Lo puedes actualizar según tu dataset

# Semilla para reproducibilidad
SEED = 42
