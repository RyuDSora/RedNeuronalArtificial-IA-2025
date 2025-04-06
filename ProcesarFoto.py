from PIL import Image
import numpy as np

#Cargar y convertir imagen en datos 
def cargar_foto(url):
    foto = Image.open(url).convert('L')   # Convertimos a escala de grises
    foto = foto.resize((32, 32))           # Redimensionar a 32x32 para que sea mas rapido
    foto_arreglo = np.asarray(foto, dtype=np.float32) / 255.0  # Normalizazamos
    return foto_arreglo.flatten().tolist()