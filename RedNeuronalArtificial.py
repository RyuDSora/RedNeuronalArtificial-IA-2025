# RedNeuronalArtificial.py
import numpy as np
from FuncionesActivacion import sigmoide, lineal, relu, tanh, softmax

class Neurona:
    def __init__(self,funcion_activacion):
        self.entradas = []  # [(origen: Neurona, peso: float)]
        self.salida = 0.0
        self.backpropagation = 0.0  # para backpropagation
        self.funcion_activacion = funcion_activacion
        self.activacion = self._get_funcion_activacion()

    def agregar_entrada(self, neurona, peso):
        self.entradas.append([neurona, peso])

    def _get_funcion_activacion(self):
        #Selecciona la función de activación que se utilizará.        
        if self.funcion_activacion == "sigmoide":
            return sigmoide
        elif self.funcion_activacion == "relu":
            return relu
        elif self.funcion_activacion == "softmax":
            return softmax
        elif self.funcion_activacion == "lineal":
            return lineal
        elif self.funcion_activacion == "tanh":
            return tanh
        raise ValueError("Función de activación no soportada")

    def activar_funcion(self, x):
        return self.activacion(x)

    def activar_neurona(self):
        total = sum(neurona.salida * peso for neurona, peso in self.entradas)
        self.salida = self.activar_funcion(total)  # salida segun la funcion de activacion dada


class Capa:        
    def __init__(self, tamanio,funcion_activacion):
        self.neuronas = [Neurona(funcion_activacion) for _ in range(tamanio)]

    def conexion(self, capa_anterior):
        for neurona in self.neuronas:
            for prev_neuron in capa_anterior.neuronas:
                neurona.agregar_entrada(prev_neuron, np.random.randn() * 0.1)

class RedNeuronalArtificial:
    def __init__(self, tamanio_inicial, tamanio_capa_oculta, tamanio_salida, funcion_activacion):
        #creamos las capas
        self.capa_entrada = Capa(tamanio_inicial,funcion_activacion)
        self.capa_oculta = Capa(tamanio_capa_oculta,funcion_activacion)
        self.capa_salida = Capa(tamanio_salida,funcion_activacion)
        
        #conectamos las capas
        self.capa_oculta.conexion(self.capa_entrada)
        self.capa_salida.conexion(self.capa_oculta)

    def propagacion(self, valores_entrada):
        # Asignar entradas directamente
        for i, value in enumerate(valores_entrada):
            self.capa_entrada.neuronas[i].salida = value
        # Propagar hacia adelante
        for layer in [self.capa_oculta, self.capa_salida]:
            for neuron in layer.neuronas:
                neuron.activar_neurona()
        return [n.salida for n in self.capa_salida.neuronas]


    def propagacionAtras(self, objetivo, tasa_aprendizaje=0.1):
        # Salida: calcular backpropagation
        for i, neuron in enumerate(self.capa_salida.neuronas):
            error = objetivo[i] - neuron.salida
            neuron.backpropagation = error * neuron.salida * (1 - neuron.salida)

        # Oculta: calcular backpropagation
        for i, neuron in enumerate(self.capa_oculta.neuronas):
            error = sum(out_neuron.backpropagation * weight for out_neuron in self.capa_salida.neuronas
                        for src, weight in out_neuron.entradas if src == neuron)
            neuron.backpropagation = error * neuron.salida * (1 - neuron.salida)

        # Actualizar pesos (salida)
        for neuron in self.capa_salida.neuronas:
            for dato in neuron.entradas:
                entrada_neurona, peso = dato
                dato[1] += tasa_aprendizaje * neuron.backpropagation * entrada_neurona.salida

        # Actualizar pesos (oculta)
        for neuron in self.capa_oculta.neuronas:
            for dato in neuron.entradas:
                entrada_neurona, weight = dato
                dato[1] += tasa_aprendizaje * neuron.backpropagation * entrada_neurona.salida

    def entrenar(self, X, y, epochs=1000, lr=0.1):
        for epoch in range(epochs):
            error_sum = 0
            for i in range(len(X)):
                salida = self.propagacion(X[i])
                error = sum((y[i][j] - salida[j])**2 for j in range(len(salida)))
                error_sum += error
                self.propagacionAtras(y[i], tasa_aprendizaje=lr)
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Error: {error_sum:.5f}")

