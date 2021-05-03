import glfw
import math
import numpy as np
import grafica.transformations as tr


class Hinata():
    # Clase que contiene el modelo del personaje del jugador
    def __init__(self, model, controller):
        self.pos = [0,-0.87] # Posicion inicial en el escenario
        self.vel = [0.7,0.7] # Velocidad del jugador
        self.model = model # Referencia al grafo de escena asociado
        self.controller = controller # Referencia del controlador, para acceder a sus variables
        self.size = 0.25 # Escala a aplicar al nodo 
        self.radio = 0.3 # distancia para realiozar los calculos de colision

    def update(self, delta):
        # Se actualiza la posicion del jugador
        
        # Si detecta la tecla [D] presionada se mueve hacia la derecha
        if self.controller.is_d_pressed and self.pos[0] < 0.635:
            self.pos[0] += self.vel[0] * delta
        # Si detecta la tecla [A] presionada se mueve hacia la izquierda
        if self.controller.is_a_pressed and self.pos[0] > -0.635:
            self.pos[0] -= self.vel[0] * delta
        # Si detecta la tecla [W] presionada y no se ha salido de la pista se mueve hacia arriba
        if self.controller.is_w_pressed and self.pos[1] < 0.87:
            self.pos[1] += self.vel[1] * delta
        # Si detecta la tecla [S] presionada y no se ha salido de la pista se mueve hacia abajo
        if self.controller.is_s_pressed and self.pos[1] > -0.87:
            self.pos[1] -= self.vel[1] * delta
       # print(self.pos[0], self.pos[1])

        # Se le aplica la transformacion de traslado segun la posicion actual
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size*0.8, self.size, 1)])

class Trees():
    
    def __init__(self,y_pos,model):
        self.y_pos = y_pos
        self.vel = 0.15
        self.model = model


    def update(self,delta):
        self.y_pos -= self.vel*delta
        if self.y_pos < -4:
            self.y_pos=4
        self.model.transform = tr.translate(0,self.y_pos,0)

class Lines():

    def __init__(self, y_pos, model):
        self.y_pos = y_pos
        self.vel = 0.15
        self.model = model

    def update(self,delta):
        self.y_pos -= self.vel*delta
        if self.y_pos < -2.2:
            self.y_pos = 2.2
        self.model.transform = tr.translate(0, self.y_pos,0)

class Human():

    def __init__(self,x_pos,vel,rango,model):
        self.pos = [x_pos, 1] 
        self.x_pos = x_pos
        self.rango = rango
        self.vel = vel
        self.size = 0.25
        self.movingLeft= True
        self.radio = 0.3
        self.model = model 

    def update(self,delta):
        self.pos[1] -=self.vel*delta
        if self.pos[0] < self.x_pos-self.rango:
            self.movingLeft = False
        if self.pos[0] > self.x_pos+self.rango:
            self.movingLeft = True
        if self.pos[0] < self.x_pos+ 0.5 and self.movingLeft:    
            self.pos[0] -= math.sin(self.vel*delta)
        if self.pos[0] < self.x_pos+ 0.5 and not self.movingLeft:    
            self.pos[0] += math.sin(self.vel*delta)    
 
        self.model.transform = tr.matmul([tr.translate(self.pos[0],self.pos[1],0), tr.scale(self.size*0.8, self.size, 1)])

    
class Zombie():

    def __init__(self,x_pos,vel,rango,model):
        self.pos = [x_pos, 1] 
        self.x_pos = x_pos
        self.rango = rango
        self.vel = vel
        self.size = 0.18
        self.movingLeft= True
        self.radio = 0.3
        self.model = model

    def update(self,delta):
        self.pos[1] -=self.vel*delta
        if self.pos[0] < self.x_pos-self.rango:
            self.movingLeft = False
        if self.pos[0] > self.x_pos+self.rango:
            self.movingLeft = True
        if self.pos[0] < self.x_pos+ 0.5 and self.movingLeft:    
            self.pos[0] -= math.sin(self.vel*delta)
        if self.pos[0] < self.x_pos+ 0.5 and not self.movingLeft:    
            self.pos[0] += math.sin(self.vel*delta)    
 
        self.model.transform = tr.matmul([tr.translate(self.pos[0],self.pos[1],0), tr.scale(self.size*0.8, self.size, 1)]) 

class Store():

    def __init__(self, y_pos,model):
        self.pos = [-0.6, y_pos]
        self.vel = 0.15
        self.size = 0.4
        self.radio = 0.3
        self.model = model
        self.model.transform = tr.matmul([tr.translate(-0.85, y_pos, 0.7), tr.rotationZ(math.pi/2),tr.scale(self.size*1.5, 0.9*self.size, 1)])

    def update(self,delta):
        self.pos[1] -= self.vel*delta
        if self.pos[1] < -2.2:
            self.pos[1] = 3
        self.model.transform = tr.matmul([tr.translate(-0.85, self.pos[1], 0), tr.rotationZ(math.pi/2),tr.scale(self.size*1.5, 0.9*self.size, 1)])
