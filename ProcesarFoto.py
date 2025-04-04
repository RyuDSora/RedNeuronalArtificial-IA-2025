from PIL import Image
import numpy as np

#Cargar y convertir imagen en datos 
def cargar_foto(url):
    foto = Image.open(url).convert('L')   # Convertimos a escala de grises
    foto = np.array(foto) / 255.0 # Convertimos en vector y normalizamos
    return foto