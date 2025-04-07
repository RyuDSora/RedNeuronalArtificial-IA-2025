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

#derivadas para la backpropagation
def derivada_sigmoide(y):
    return y * (1 - y)
def derivada_relu(y):
    return 1.0 * (y > 0)
def derivada_tanh(y):
    return 1 - y**2
def derivada_lineal(y):
    return 1

