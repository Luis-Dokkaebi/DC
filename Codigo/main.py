# Codigo/main.py

import os

# Solución para error "OMP: Error #15: Initializing libomp.dll..."
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn
import torch.optim as optim
from Codigo import config
from Codigo.utils import data_loader
from Codigo import modelo_cnn

# Configurar dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Usando dispositivo: {device}")

# Semilla
torch.manual_seed(config.SEED)

# Cargar datos
train_loader, val_loader, clases = data_loader.get_data_loaders()
print(f"Clases detectadas: {clases}")

if len(clases) < 2:
    print("\n❌ ERROR CRÍTICO: Se necesitan al menos 2 clases para entrenar (ej. 'Grieta' y 'Sin_Grieta').")
    print("   Actualmente solo se detectó una clase. Agrega más carpetas en 'Imagenes/' con ejemplos negativos.\n")
    exit(1)

# Crear modelo
modelo = modelo_cnn.CNNBasica(num_classes=len(clases)).to(device)

# Pérdida y optimizador
criterio = nn.CrossEntropyLoss()
optimizador = optim.Adam(modelo.parameters(), lr=config.LEARNING_RATE)

# Entrenamiento
for epoch in range(config.EPOCHS):
    modelo.train()
    total_loss = 0

    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)

        optimizador.zero_grad()
        salida = modelo(imgs)
        loss = criterio(salida, labels)
        loss.backward()
        optimizador.step()

        total_loss += loss.item()

    print(f"🎓 Época {epoch+1}/{config.EPOCHS}, Pérdida: {total_loss:.4f}")

# Evaluación
modelo.eval()
correctos = 0
total = 0

with torch.no_grad():
    for imgs, labels in val_loader:
        imgs, labels = imgs.to(device), labels.to(device)
        salida = modelo(imgs)
        _, predicciones = torch.max(salida, 1)
        total += labels.size(0)
        correctos += (predicciones == labels).sum().item()

precision = 100 * correctos / total
print(f"✨ Precisión en validación: {precision:.2f}%")

# Guardar modelo
os.makedirs(config.MODELOS_DIR, exist_ok=True)
modelo_path = os.path.join(config.MODELOS_DIR, 'modelo_cnn.pth')
torch.save(modelo.state_dict(), modelo_path)
print(f"💾 Modelo guardado en: {modelo_path}")

# Guardar lista de clases
clases_path = os.path.join(config.MODELOS_DIR, 'clases.txt')
with open(clases_path, 'w') as f:
    for c in clases:
        f.write(c + '\n')
print(f"📋 Lista de clases guardada en: {clases_path}")
