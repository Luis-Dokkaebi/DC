# Codigo/modelo_cnn.py

import torch
import torch.nn as nn
import torch.nn.functional as F
from Codigo import config

class CNNBasica(nn.Module):
    def __init__(self, num_classes=None):
        super(CNNBasica, self).__init__()

        if num_classes is None:
            num_classes = config.NUM_CLASSES

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.25)

        # Suponiendo imagenes de 128x128
        self.fc1 = nn.Linear(128 * (config.IMAGE_SIZE[0] // 8) * (config.IMAGE_SIZE[1] // 8), 256)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))   # 128x128 -> 64x64
        x = self.pool(F.relu(self.conv2(x)))   # 64x64 -> 32x32
        x = self.pool(F.relu(self.conv3(x)))   # 32x32 -> 16x16
        x = self.dropout(x)

        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return x
