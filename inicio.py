import ProcesarFoto as pf
from RedNeuronalArtificial import RedNeuronalArtificial


dataset = [
    ("train.jpg", 1)

]

#print(dataset)
foto_ancho = 600
foto_alto = 800
tamanio_entrada = foto_ancho*foto_alto
capas_ocultas = [100,50,203]
tamanio_salida = 1
funcion_activacion = 'sigmoide' #sigmoide, relu,  lineal, tanh
epochs = 100
tasa_aprendizaje = 0.1

X = [pf.cargar_foto(url, foto_ancho, foto_alto) for url, objetivo in dataset]

#print(X)

y = [[objetivo] for url, objetivo in dataset]

#print(y)

nn = RedNeuronalArtificial(tamanio_entrada,capas_ocultas,tamanio_salida,funcion_activacion)
nn.entrenar(X, y, epochs, tasa_aprendizaje)

fotos_prueba = ["test1.jpg", 
                "test2.jpg", 
                'test3.jpg']

for url in fotos_prueba:
    result = nn.propagacion(pf.cargar_foto(url, foto_ancho, foto_alto))
    pred = "MISMA persona" if result[0] > 0.8 else "DIFERENTE persona"
    print(f"{url} → {pred} ({result[0]*100:.0f}%)")