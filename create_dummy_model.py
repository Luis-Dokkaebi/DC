import torch
import os
from Codigo.modelo_cnn import CNNBasica
from Codigo import config

def create_dummy_model():
    os.makedirs(config.MODELOS_DIR, exist_ok=True)
    model = CNNBasica(num_classes=3) # match dummy data classes
    torch.save(model.state_dict(), os.path.join(config.MODELOS_DIR, 'modelo_cnn.pth'))
    print("Dummy model created.")

if __name__ == "__main__":
    create_dummy_model()
