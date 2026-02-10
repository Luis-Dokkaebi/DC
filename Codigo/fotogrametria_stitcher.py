import cv2
import os
import sys
import numpy as np

# Configurar ruta para poder ejecutarse independientemente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def unir_imagenes(carpeta_imagenes, salida="Resultados/panorama.png"):
    """
    Intenta unir imágenes en una panorámica (Stitching básico).
    NOTA: Esto requiere solapamiento entre las fotos y características comunes.
    """
    print(f"📷 Cargando imágenes desde: {carpeta_imagenes}")
    imagenes = []

    # Cargar imágenes
    if not os.path.exists(carpeta_imagenes):
        print(f"❌ La carpeta '{carpeta_imagenes}' no existe.")
        return

    archivos = sorted(os.listdir(carpeta_imagenes))
    if not archivos:
        print("❌ No hay imágenes en la carpeta.")
        return

    for archivo in archivos:
        if archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            ruta = os.path.join(carpeta_imagenes, archivo)
            img = cv2.imread(ruta)
            if img is not None:
                # Redimensionar para velocidad (opcional)
                #img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
                imagenes.append(img)
            else:
                print(f"⚠️ No se pudo cargar {archivo}")

    if len(imagenes) < 2:
        print("❌ Se necesitan al menos 2 imágenes para unir.")
        return

    print(f"🧩 Intentando unir {len(imagenes)} imágenes...")

    # Crear el stitcher (OpenCV 4+)
    stitcher = cv2.Stitcher_create()

    # Intentar unir
    status, pano = stitcher.stitch(imagenes)

    if status == cv2.Stitcher_OK:
        print("✅ ¡Éxito! Panorámica creada.")

        # Guardar resultado
        os.makedirs(os.path.dirname(salida), exist_ok=True)
        cv2.imwrite(salida, pano)
        print(f"💾 Guardado en: {salida}")
    else:
        errores = {
            cv2.Stitcher_ERR_NEED_MORE_IMGS: "Se necesitan más imágenes",
            cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "Fallo al estimar homografía (no se encontraron suficientes coincidencias)",
            cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "Fallo al ajustar parámetros de cámara"
        }
        mensaje = errores.get(status, f"Error desconocido (código {status})")
        print(f"❌ Falló el stitching: {mensaje}")
        print("💡 Consejo: Asegúrate de que las fotos tengan suficiente solapamiento (60-80%) y buena iluminación.")

if __name__ == "__main__":
    # Ejemplo de uso:
    # Asegúrate de tener una carpeta con fotos solapadas en 'Datos/Panoramica_Test' o similar.
    # Por defecto usaremos 'Datos' si el usuario pone fotos allí.
    carpeta = "Datos"
    unir_imagenes(carpeta)
