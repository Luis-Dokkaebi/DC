# Codigo/utils/visualiza_dataset.py

import os
import matplotlib.pyplot as plt
import torchvision
from torchvision import transforms
from Codigo import config

def visualizar_dataset(num_imagenes=8):
    transform = transforms.Compose([
        transforms.Resize(config.IMAGE_SIZE),
        transforms.ToTensor()
    ])

    dataset = torchvision.datasets.ImageFolder(root=config.IMAGENES_DIR, transform=transform)
    clases = dataset.classes

    loader = torch.utils.data.DataLoader(dataset, batch_size=num_imagenes, shuffle=True)
    data_iter = iter(loader)
    imagenes, etiquetas = next(data_iter)

    # Mostrar imágenes
    fig, axes = plt.subplots(1, num_imagenes, figsize=(15, 3))
    for i in range(num_imagenes):
        img = imagenes[i].permute(1, 2, 0)  # Reordenar dimensiones a HWC
        img = img * 0.5 + 0.5  # Desnormalizar si normalizaste entre -1 y 1
        axes[i].imshow(img)
        axes[i].set_title(clases[etiquetas[i]])
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import torch
    visualizar_dataset()
