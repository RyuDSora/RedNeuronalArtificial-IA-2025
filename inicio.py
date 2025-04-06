import ProcesarFoto as pf
from RedNeuronalArtificial import RedNeuronalArtificial


dataset = [
    ("Nueva/train.jpg", 1),
    ("Nueva/train2.jpg", 1),
    ("Nueva/train3.jpg", 1),
    ("Nueva/train4.jpg", 0),
    ("Nueva/train5.jpg", 0)
]

#print(dataset)

tamanio_entrada = 32*32
tamanio_oculta = 32
tamanio_salida = 1
funcion_activacion = 'sigmoide' #sigmoide, relu, softmax, lineal, tanh
epochs = 1000
tasa_aprendizaje = 0.1

X = [pf.cargar_foto(url) for url, objetivo in dataset]

#print(X)

y = [[objetivo] for url, objetivo in dataset]

#print(y)

nn = RedNeuronalArtificial(tamanio_entrada,tamanio_oculta,tamanio_salida,funcion_activacion)
nn.entrenar(X, y, epochs, tasa_aprendizaje)

fotos_prueba = ["Nueva/test1.jpg", "Nueva/test2.jpg", 'Nueva/test3.jpg']

for path in fotos_prueba:
    result = nn.propagacion(pf.cargar_foto(path))
    pred = "MISMA persona" if result[0] > 0.8 else "DIFERENTE persona"
    print(f"{path} → {pred} ({result[0]:.4f})")