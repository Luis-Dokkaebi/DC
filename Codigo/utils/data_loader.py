# Codigo/utils/data_loader.py

import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from Codigo import config

def get_data_loaders(image_size=None, batch_size=None):
    # Usa valores del config si no se dan directamente
    if image_size is None:
        image_size = config.IMAGE_SIZE
    if batch_size is None:
        batch_size = config.BATCH_SIZE

    # Transformaciones de datos
    transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])  # Para imágenes en escala de grises o ajusta si es RGB
    ])

    # Carga de datos
    dataset = datasets.ImageFolder(root=config.IMAGENES_DIR, transform=transform)

    # Separación simple en entrenamiento y validación
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    # DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, dataset.classes
