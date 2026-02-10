# Explicación del Proyecto en Lenguaje Natural

Este proyecto es una aplicación de inteligencia artificial que utiliza una red neuronal convolucional (CNN) para clasificar imágenes. Además, tiene la capacidad de generar reportes automáticos en Word y PDF con los resultados de la clasificación.

## Resumen del Proyecto
El proyecto está diseñado para:
1.  **Entrenar** un modelo de aprendizaje profundo para reconocer diferentes clases de imágenes.
2.  **Usar** ese modelo para clasificar nuevas imágenes.
3.  **Generar** reportes visuales y documentales de las predicciones.

## Estructura de Carpetas
- **Codigo/**: Contiene todo el código fuente del proyecto.
- **Datos/**: Aquí se colocan las nuevas imágenes que se quieren clasificar.
- **Imagenes/**: Dataset de entrenamiento, donde cada subcarpeta es una clase diferente.
- **Modelos/**: Donde se guardan los modelos entrenados (.pth).
- **Resultados/**: Donde se guardan los reportes y salidas generadas.
- **utils/**: Funciones auxiliares para cargar datos, verificar imágenes, etc.

## Explicación de los Archivos Principales

### 1. `Codigo/main.py` (Entrenamiento)
Este es el script principal para entrenar la red neuronal.
- **Carga de datos**: Usa `utils.data_loader` para leer las imágenes de la carpeta `Imagenes/`, transformarlas (redimensionar, normalizar) y dividirlas en conjuntos de entrenamiento y validación.
- **Creación del modelo**: Inicializa la arquitectura definida en `modelo_cnn.py`.
- **Entrenamiento**: Itera sobre los datos varias veces (épocas), ajustando los pesos del modelo para minimizar el error (pérdida) entre la predicción y la etiqueta real.
- **Evaluación**: Al final, mide la precisión del modelo en el conjunto de validación.
- **Guardado**: Guarda el modelo entrenado en la carpeta `Modelos/` con el nombre `modelo_cnn.pth`.

### 2. `Codigo/modelo_cnn.py` (Arquitectura)
Define la estructura de la red neuronal convolucional `CNNBasica`.
- **Capas Convolucionales (`conv1`, `conv2`, `conv3`)**: Extraen características visuales de la imagen (bordes, texturas, formas).
- **Pooling (`pool`)**: Reduce el tamaño espacial de las características para hacer el cálculo más eficiente.
- **Capas Completamente Conectadas (`fc1`, `fc2`)**: Toman las características extraídas y realizan la clasificación final en una de las clases posibles.
- **Dropout**: Ayuda a evitar el sobreajuste durante el entrenamiento apagando aleatoriamente algunas neuronas.

### 3. `Codigo/generar_reporte.py` (Inferencia y Reportes)
Este script usa el modelo ya entrenado para clasificar nuevas imágenes.
- **Carga del modelo**: Lee el archivo `.pth` guardado anteriormente.
- **Clasificación**: Recorre todas las imágenes en la carpeta `Datos/`, las procesa y predice su clase.
- **Generación de Reportes**:
    - **Gráfica**: Crea un gráfico de barras mostrando cuántas imágenes hay de cada clase.
    - **Word**: Genera un documento `.docx` con una tabla resumen y el detalle de cada imagen clasificada (incluyendo la imagen marcada con su etiqueta).
    - **PDF**: Genera un archivo `.pdf` con información similar.

### 4. `Codigo/config.py` (Configuración)
Centraliza los parámetros del proyecto para facilitar cambios.
- Define rutas de carpetas (`IMAGENES_DIR`, `MODELOS_DIR`, etc.).
- Define hiperparámetros como el tamaño de imagen (`IMAGE_SIZE`), tamaño de lote (`BATCH_SIZE`), tasa de aprendizaje (`LEARNING_RATE`) y número de épocas (`EPOCHS`).

### 5. `Codigo/utils/data_loader.py` (Utilidad)
Se encarga de preparar los datos para el entrenamiento.
- Define las transformaciones necesarias para las imágenes.
- Carga las imágenes desde las carpetas.
- Divide el dataset en entrenamiento (80%) y validación (20%).
- Crea los `DataLoaders` que entregan los datos en lotes al modelo.

---
Esta explicación cubre los aspectos fundamentales del código y cómo interactúan las diferentes partes para lograr el objetivo de clasificación y reporte.
