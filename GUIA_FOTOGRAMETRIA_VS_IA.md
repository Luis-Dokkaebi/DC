# Guía: Fotogrametría vs. Inteligencia Artificial (IA)

Esta guía aclara las diferencias fundamentales entre **Clasificación (lo que hace tu modelo actual)** y **Fotogrametría (crear modelos 3D y mapas)**, y cómo puedes empezar a usar tus fotos para ambos propósitos.

---

## 1. Clasificación de Imágenes (Lo que tienes ahora)
- **Objetivo:** Responder preguntas como *"¿Qué es esta foto?"* (Ej. Cimentación vs Estructura).
- **Cómo funciona:** Usas una Red Neuronal (CNN) entrenada con ejemplos etiquetados.
- **Uso:** Medir avance de obra, detectar anomalías, contar objetos.

## 2. Fotogrametría (Lo que quieres hacer)
- **Objetivo:** Convertir fotos 2D en modelos 3D, mapas topográficos y ortofotos (mapas planos gigantes).
- **Cómo funciona:** No usa "inteligencia artificial" en el sentido tradicional, sino **geometría**. Busca puntos comunes en fotos solapadas (Structure from Motion - SfM) para triangular la posición de cada pixel en el espacio 3D.
- **Requiere:**
    - Solapamiento entre fotos (60-80%).
    - GPS en las fotos (normalmente los drones lo incluyen).

### ¿Se puede "enseñar" a la IA a hacer fotogrametría?
Tradicionalmente **NO**. La fotogrametría es matemática pura. Sin embargo, la **IA moderna (NeRFs, Gaussian Splatting)** está revolucionando esto.
- **NeRF (Neural Radiance Fields):** Entrena una pequeña red neuronal para *representar* la escena 3D.
- **Gaussian Splatting:** Nueva técnica muy rápida para visualizar escenas 3D aprendidas.

---

## 3. Tu Hoja de Ruta

### A) Opción Profesional (Recomendada)
Para obtener planos métricos precisos y modelos 3D exportables a AutoCAD/Revit:
1.  **Software Open Source:** Instala **WebODM** (OpenDroneMap). Es el estándar de oro libre.
2.  **Software Comercial:** Pix4D, Agisoft Metashape.
3.  **Proceso:** Subes tus fotos -> El software procesa -> Descargas el modelo 3D (.obj) y la Ortofoto (.tif).

### B) Opción "Hazlo tú mismo" con Python (Básica)
Si quieres experimentar programando algo sencillo, puedes hacer "Stitching" (unir fotos) para crear panorámicas planas.
- **Hemos incluido un script básico:** `Codigo/fotogrametria_stitcher.py`.
- **Limitación:** No crea modelos 3D con volumen, solo une imágenes planas.

---

## 4. Conclusión
- Usa tu código actual (`main.py`) para saber **EN QUÉ ETAPA** está la obra.
- Usa herramientas de Fotogrametría (como WebODM) para saber **CUÁNTO MIDE** la obra y verla en 3D.
- Si quieres experimentar con IA 3D, busca tutoriales sobre "Nerfstudio" o "Gaussian Splatting", pero requieren hardware potente (GPU NVIDIA).
