# RedNeuronalArtificial.py
import numpy as np
from FuncionesActivacion import sigmoide, lineal, relu, tanh
from FuncionesActivacion import derivada_sigmoide, derivada_relu, derivada_tanh, derivada_lineal

class Neurona:
    def __init__(self,funcion_activacion):
        self.entradas = []  # [(origen: Neurona, peso: float)]
        self.salida = 0.0
        self.backpropagation = 0.0  # para backpropagation
        self.funcion_activacion = funcion_activacion
        self.sesgo = np.random.randn()
        self.activacion, self.derivada = self._get_funciones()

    def agregar_entrada(self, neurona, peso):
        self.entradas.append([neurona, peso])

    def _get_funciones(self):
        #Selecciona la función de activación que se utilizará.        
        if self.funcion_activacion == "sigmoide":
            return sigmoide, derivada_sigmoide
        elif self.funcion_activacion == "relu":
            return relu, derivada_relu
        elif self.funcion_activacion == "lineal":
            return lineal, derivada_lineal
        elif self.funcion_activacion == "tanh":
            return tanh, derivada_tanh
        raise ValueError("Función de activación no soportada")

    def activar_neurona(self):
        total = sum(neurona.salida * peso for neurona, peso in self.entradas)
        total += self.sesgo
        self.salida = self.activacion(total) # salida segun la funcion de activacion dada


class Capa:        
    def __init__(self, tamanio,funcion_activacion):
        self.neuronas = [Neurona(funcion_activacion) for _ in range(tamanio)]

    def conexion(self, capa_anterior):
        for neurona in self.neuronas:
            for prev_neuron in capa_anterior.neuronas:
                neurona.agregar_entrada(prev_neuron, np.random.randn() * 0.1)

class RedNeuronalArtificial:
    def __init__(self, tamanio_inicial, capas_ocultas, tamanio_salida, funcion_activacion):
        
        #creamos las capas
        #capa de entrada
        self.capa_entrada = Capa(tamanio_inicial,funcion_activacion)

        #capas ocultas
        self.capas_ocultas = []
        capa_anterior = self.capa_entrada
        for tamanio_oculta in capas_ocultas:
            #creamos las capas ocultas segun la lista
            nueva_capa_oculta = Capa(tamanio_oculta, funcion_activacion)

            #la conectamos con la ultima capa
            nueva_capa_oculta.conexion(capa_anterior)
            self.capas_ocultas.append(nueva_capa_oculta)
            capa_anterior = nueva_capa_oculta
        
        #capa de salida
        self.capa_salida = Capa(tamanio_salida, funcion_activacion)

        #conectamos con la ultima capa(si hay capa oculta la conectara con la ultima oculta, si no hay ninguna 
        #conectara la salida directamente con la entrada)
        self.capa_salida.conexion(capa_anterior)
            
        
    def propagacion(self, valores_entrada):
        # Asignar entradas directamente
        for i, valor in enumerate(valores_entrada):
            self.capa_entrada.neuronas[i].salida = valor

        # Propagar hacia adelante
        for capa in self.capas_ocultas:
            for neurona in capa.neuronas:
                neurona.activar_neurona()

        for neurona in self.capa_salida.neuronas:
            neurona.activar_neurona()

        return [n.salida for n in self.capa_salida.neuronas]

    def propagacionAtras(self, objetivo, tasa_aprendizaje=0.1):
        # Salida: calcular backpropagation
        for i, neurona in enumerate(self.capa_salida.neuronas):
            error = objetivo[i] - neurona.salida
            neurona.backpropagation = error * neurona.derivada(neurona.salida)

        # Oculta: calcular backpropagation, Capas ocultas (en orden inverso)
        for capa in reversed(self.capas_ocultas):
            for neurona in capa.neuronas:
                error = sum(out_neurona.backpropagation * peso for out_neurona in self.capa_salida.neuronas
                            for src, peso in out_neurona.entradas if src == neurona)
                neurona.backpropagation = error * neurona.derivada(neurona.salida)

        # Actualizar pesos (salida)
        for neurona in self.capa_salida.neuronas:
            for entrada in neurona.entradas:
                entrada_neurona, peso = entrada
                entrada[1] += tasa_aprendizaje * neurona.backpropagation * entrada_neurona.salida
            
            neurona.sesgo += tasa_aprendizaje * neurona.backpropagation

        # Actualizar pesos (oculta)
        for capa in self.capas_ocultas:
            for neurona in capa.neuronas:
                for entrada in neurona.entradas:
                    entrada_neurona, peso = entrada
                    entrada[1] += tasa_aprendizaje * neurona.backpropagation * entrada_neurona.salida
                neurona.sesgo += tasa_aprendizaje * neurona.backpropagation

    def entrenar(self, X, y, epochs=1000, lr=0.1):
        for epoch in range(epochs):
            error_total = 0
            for i in range(len(X)):
                salida = self.propagacion(X[i])
                error = sum((y[i][j] - salida[j])**2 for j in range(len(salida)))
                error_total += error
                self.propagacionAtras(y[i], tasa_aprendizaje=lr)
            if epoch % 1 == 0:
                print(f"Epoch {epoch}, Error: {error_total:.6f}")
                yield [epoch,error_total]

