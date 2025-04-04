#Funciones de activacion para una red neuronal
import math

#funcion lineal 
# f(x) = x
def lineal(x):
    return x

#sigmoide 
# f(x) = 1/(1 + e^-x)
def sigmoide(x):
    return 1 / (1 + math.exp(-x))

#tangente hiperbólica (tanh) 
# f(x) = (e^x - e^ - x)/(e^x + e^ - x)
def tanh(x):
    return (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))

#Activación de unidad lineal rectificada (ReLU)
# f(x) = max(0, x)
def relu(x):
    return max(0, x)

#Activación softmax
#f(xi) = e^xi/Σj e^xj
def softmax(x):
    valores_de_X = [math.exp(i) for i in x]
    suma_de_valores_de_X = sum(valores_de_X)
    return [i / suma_de_valores_de_X for i in valores_de_X]

