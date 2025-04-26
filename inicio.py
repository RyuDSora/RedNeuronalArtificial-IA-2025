import ProcesarFoto as pf
from RedNeuronalArtificial import RedNeuronalArtificial

#train persona
#train2 persona
#train3 persona
#train4 diferente
#train5 diferente
#("train.jpg", 1)
#("train2.jpg", 1)
#("train3.jpg", 1)
#("train4.jpg", 0)
#("train5.jpg", 0)


dataset = [
    ("train.jpg", 1),
    ("train3.jpg", 1),
    ("train4.jpg", 0),
    ("train5.jpg", 0)

]

#print(dataset)
escala = 0.1 #escala de 10%
foto_ancho = int(600*escala)
foto_alto = int(800*escala)
tamanio_entrada = foto_ancho*foto_alto
capas_ocultas = [100,50]
tamanio_salida = 1
funcion_activacion = 'sigmoide' #sigmoide, relu,  lineal, tanh
epochs = 1500
tasa_aprendizaje = 0.1

X = [pf.cargar_foto(url, foto_ancho, foto_alto) for url, objetivo in dataset]

#print(X)

y = [[objetivo] for url, objetivo in dataset]

#print(y)

nn = RedNeuronalArtificial(tamanio_entrada,capas_ocultas,tamanio_salida,funcion_activacion)
nn.entrenar(X, y, epochs, tasa_aprendizaje)

#test1 --> misma persona
#test2 --> diferente persona
#test3 --> misma persona

fotos_prueba = ["test1.jpg", 
                "test2.jpg", 
                'test3.jpg']

for url in fotos_prueba:
    result = nn.propagacion(pf.cargar_foto(url, foto_ancho, foto_alto))
    pred = "MISMA persona" if result[0] > 0.5 else "DIFERENTE persona"
    print(f"{url} → {pred} ({result[0]*100:.0f}%)")