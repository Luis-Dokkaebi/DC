# DronConstruccion
# 🛠️ Proyecto: Reconocimiento de Imágenes con Red Neuronal Personalizada

Este proyecto permite entrenar una red neuronal convolucional (CNN) personalizada para clasificar imágenes, y luego usar ese modelo entrenado para analizar nuevas imágenes, generar predicciones y reportes automáticos (en Word y PDF).

## 📁 Estructura del proyecto

DronConstruccion/
├── Imagenes/ # Dataset de entrenamiento, una carpeta por clase

├── Datos/ # Imágenes nuevas para clasificar con el modelo entrenado

├── Codigo/ # Código fuente: redes, carga, entrenamiento y reportes

│──├── utils/ # Funciones auxiliares: carga de datos, visualización, etc.

├── Modelos/ # Archivos del modelo entrenado (.pth)

├── Resultados/ # Reportes generados y salidas visuales

## 🧪 Tecnologías

- Python 🐍
- OpenCV
- PyTorch / torchvision
- Matplotlib

## 🚀 Flujo de trabajo

1. Coloca tus datos de entrenamiento en `Imagenes/`, una subcarpeta por clase.
2. Corre `Codigo/main.py` para entrenar tu modelo.
3. Coloca imágenes nuevas en `Datos/`.
4. Corre `Codigo/generar_reporte.py` para:
   - Clasificar nuevas imágenes.
   - Generar un reporte `.docx` y `.pdf`.
   - Guardar imágenes etiquetadas y gráficas.

## 💾 Requisitos principales

```bash
pip install torch torchvision matplotlib python-docx reportlab
