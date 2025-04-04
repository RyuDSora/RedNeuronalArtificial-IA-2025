# prueba.py

import ProcesarFoto as pf
import matplotlib.pyplot as plt
import pandas as pd

# Cargar dos imágenes
img1 = pf.cargar_foto('persona_otro_angulo.jpg')
img2 = pf.cargar_foto('otra_persona.jpg')

# Convertir a DataFrames para visualización (opcional si solo quieres usar plt.imshow)
imagen1 = pd.DataFrame(img1)
imagen2 = pd.DataFrame(img2)

# Mostrar lado a lado
fig, axes = plt.subplots(1, 2, figsize=(20, 10))  # 1 fila, 2 columnas

# Primera imagen
axes[0].imshow(imagen1, cmap='gray')
axes[0].set_title("Imagen 1")
axes[0].axis('off')  # Ocultar ejes

# Segunda imagen
axes[1].imshow(imagen2, cmap='gray')
axes[1].set_title("Imagen 2")
axes[1].axis('off')

# Mostrar ambas
plt.tight_layout()
plt.show()
