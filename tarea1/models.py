import glfw
import numpy as np
import grafica.transformations as tr


class Hinata():
    # Clase que contiene el modelo del personaje del jugador
    def __init__(self):
        self.pos = [0,-0.9] # Posicion inicial en el escenario
        self.vel = [1,1] # Velocidad del jugador
        self.model = None # Referencia al grafo de escena asociado
        self.controller = None # Referencia del controlador, para acceder a sus variables
        self.size = 0.3 # Escala a aplicar al nodo 
        self.radio = 0.2 # distancia para realiozar los calculos de colision

    def set_model(self, new_model):
        # Se relaciona a un nodo
        self.model = new_model
    
    def set_controller(self, new_controller):
        # Se relaciona a un controlador
        self.controller = new_controller

    def update(self, delta):
        # Se actualiza la posicion del jugador
        
        # Si detecta la tecla [D] presionada se mueve hacia la derecha
        if self.controller.is_d_pressed and self.pos[0] < 0.65:
            self.pos[0] += self.vel[0] * delta
        # Si detecta la tecla [A] presionada se mueve hacia la izquierda
        if self.controller.is_a_pressed and self.pos[0] > -0.62:
            self.pos[0] -= self.vel[0] * delta
        # Si detecta la tecla [W] presionada y no se ha salido de la pista se mueve hacia arriba
        if self.controller.is_w_pressed and self.pos[1] < 0.85:
            self.pos[1] += self.vel[1] * delta
        # Si detecta la tecla [S] presionada y no se ha salido de la pista se mueve hacia abajo
        if self.controller.is_s_pressed and self.pos[1] > -0.85:
            self.pos[1] -= self.vel[1] * delta
        print(self.pos[0], self.pos[1])

        # Se le aplica la transformacion de traslado segun la posicion actual
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])