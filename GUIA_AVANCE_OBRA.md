# Guía para Medir Avance de Obra y Aprendizaje Continuo

Este documento explica cómo utilizar la infraestructura actual de Inteligencia Artificial para cumplir dos nuevos objetivos clave:
1.  **Medir el avance de obra** a partir de las fotos del dron.
2.  **Aprendizaje continuo**: Que el sistema mejore con el tiempo usando las nuevas fotos.

## 1. Medir Avance de Obra

Para que la IA entienda el concepto de "avance", debemos traducir las etapas constructivas a **clases** que el modelo pueda diferenciar.

### Estrategia de Carpetas (Clases)
En lugar de clases genéricas, organiza tus carpetas de entrenamiento (`Imagenes/`) representando las fases cronológicas de la obra.

**Ejemplo de estructura recomendada:**
```
Imagenes/
    0_Terreno_Limpio/      (Representa 0% de avance)
    1_Cimentacion/         (Representa 20% de avance)
    2_Estructura_Muros/    (Representa 40% de avance)
    3_Techado_Losa/        (Representa 60% de avance)
    4_Obra_Negra/          (Representa 80% de avance)
    5_Acabados_Finales/    (Representa 100% de avance)
```

### Cómo funciona el cálculo
Una vez entrenado el modelo con estas carpetas:
1.  El dron toma una foto.
2.  El modelo clasifica la imagen, por ejemplo, detecta que es `2_Estructura_Muros`.
3.  El sistema asigna el porcentaje asociado (40%).
4.  Si el dron toma 100 fotos en un vuelo, se puede calcular un **promedio ponderado** o reportar el avance predominante en diferentes zonas.

---

## 2. Aprendizaje Continuo (Ciclo de Mejora)

El "aprendizaje conforme su programación" se logra mediante un ciclo de retroalimentación activa. El modelo no aprende solo "en vivo", sino que necesita ser re-entrenado con las nuevas experiencias (fotos) validadas.

### Flujo de Trabajo (Workflow)

1.  **Captura (Vuelo del Dron):**
    - El dron sobrevuela y guarda fotos nuevas en la carpeta `Datos/`.

2.  **Clasificación Automática (Inferencia):**
    - Ejecutas `Codigo/generar_reporte.py` (o el nuevo script de avance).
    - La IA predice qué etapa es cada foto.

3.  **Verificación Humana (Auditoría):**
    - Un experto (ingeniero/arquitecto) revisa las carpetas de resultados o el reporte.
    - **Importante:** Si la IA se equivocó (ej. dijo "Cimentación" pero ya era "Estructura"), el experto mueve esa foto a la carpeta correcta en `Imagenes/2_Estructura_Muros`.
    - Si la IA acertó, también puedes mover la foto a su carpeta correspondiente para reforzar el conocimiento.

4.  **Re-Entrenamiento (Aprendizaje):**
    - Una vez que hayas agregado las nuevas fotos corregidas a `Imagenes/`, ejecutas nuevamente `Codigo/main.py`.
    - El modelo estudiará las nuevas fotos y ajustará sus "neuronas" para reconocer mejor esa etapa en el futuro.
    - Guardará una nueva versión de `modelo_cnn.pth` más inteligente.

### Resumen del Ciclo
`Vuelo -> Clasificación -> Corrección Manual -> Re-entrenamiento -> Mejor IA`

---

## Implementación Técnica

Se ha creado un script de demostración llamado `Codigo/demo_avance.py` que:
1.  Define un diccionario de `ETAPAS` con sus porcentajes.
2.  Carga el modelo actual.
3.  Analiza las fotos en `Datos/`.
4.  Calcula y muestra el **Avance Estimado del Proyecto**.

Puedes usar este script como base para personalizar los reportes de avance de tu obra.
