import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from shapes import *
from models import *
from grafica.assets_path import getAssetPath


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# Clase controlador con variables para manejar el estado de ciertos botones
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False


# we will use the global controller as communication with the callback function
controller = Controller()

# This function will be executed whenever a key is pressed or released
def on_key(window, key, scancode, action, mods):
    
    global controller
    
    # Caso de detectar la tecla [W], actualiza estado de variable
    if key == glfw.KEY_W:
        if action ==glfw.PRESS:
            controller.is_w_pressed = True
        elif action == glfw.RELEASE:
            controller.is_w_pressed = False

    # Caso de detectar la tecla [S], actualiza estado de variable
    if key == glfw.KEY_S:
        if action ==glfw.PRESS:
            controller.is_s_pressed = True
        elif action == glfw.RELEASE:
            controller.is_s_pressed = False

    # Caso de detectar la tecla [A], actualiza estado de variable
    if key == glfw.KEY_A:
        if action ==glfw.PRESS:
            controller.is_a_pressed = True
        elif action == glfw.RELEASE:
            controller.is_a_pressed = False

    # Caso de detectar la tecla [D], actualiza estado de variable
    if key == glfw.KEY_D:
        if action ==glfw.PRESS:
            controller.is_d_pressed = True
        elif action == glfw.RELEASE:
            controller.is_d_pressed = False

    # Caso de detecar la barra espaciadora, se cambia el metodo de dibujo
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.fillPolygon = not controller.fillPolygon

    # Caso en que se cierra la ventana
    elif key == glfw.KEY_ESCAPE and action ==glfw.PRESS:
        glfw.set_window_should_close(window, True)



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Creating a glfw window
    width = 1500
    height = 950
    title = "Tarea 1 - Beaucheffvile"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Pipeline para dibujar shapes con colores interpolados
    pipeline = es.SimpleTransformShaderProgram()
    # Pipeline para dibujar shapes con texturas
    tex_pipeline = es.SimpleTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    # Grafo de escena del background
    mainScene = createScene(pipeline)
    textureScene = createTextureScene(tex_pipeline)


    hinataImage = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, getAssetPath("boy.png"))
    hinataNode = sg.SceneGraphNode("hinata")
    hinataNode.childs = [hinataImage]

    # Se instancia el modelo del auto
    player = Hinata(hinataNode,controller)
    # Se indican las referencias del nodo y el controller al modelo
   # player.set_model(hinataNode)
   
   # player.set_controller(controller)


    # Shape con textura de la carga
    zombieImage = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, getAssetPath("zombie.png"))
    humanImage = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, getAssetPath("man.png"))
    storeImage = createTextureGPUShape(bs.createTextureQuad(1,1),tex_pipeline, getAssetPath("store.png"))

    # Se crean dos nodos de carga
    humanNode = sg.SceneGraphNode("human")
    humanNode.childs = [humanImage]
    human = Human(0,0.1,0.3,humanNode)

    zombieNode = sg.SceneGraphNode("zombie")
    zombieNode.childs = [zombieImage]
    zombie = Zombie(-0.2,0.1,0.2, zombieNode)

    storeNode = sg.SceneGraphNode("store")
    storeNode.childs = [storeImage]
    store = Store(3,storeNode)

    #garbage1Node = sg.SceneGraphNode("garbage1")
    #garbage1Node.childs = [garbage]

    #garbage2Node = sg.SceneGraphNode("garbage2")
    #garbage2Node.childs = [garbage]

    # Se crean el grafo de escena con textura y se agregan las cargas
    tex_scene = sg.SceneGraphNode("textureScene")
    #tex_scene.childs = [garbage1Node, garbage2Node]
    tex_scene.childs = [hinataNode,textureScene,humanNode,zombieNode,storeNode]
    # Se crean los modelos de la carga, se indican su nodo y se actualiza la posicion fija
    # carga1 = Carga(0.2, -0.55, 0.1)
    #carga1.set_model(garbage1Node)
    treesNode = sg.findNode(tex_scene,"first trees")
    trees2Node = sg.findNode(tex_scene,"second trees")
    trees2 = Trees(4,trees2Node)
    trees1 = Trees(0,treesNode)
    #carga2 = Carga(0.7, -0.75, 0.1)
    #carga2.set_model(garbage2Node)
    #carga2.update()
    linesNode = sg.findNode(mainScene, "first middleLines")
    lines2Node = sg.findNode(mainScene, "second middleLines")

    lines1 = Lines(0,linesNode)
    lines2 = Lines(2.2,lines2Node)
    # Lista con todas las cargas
    #cargas = [carga1, carga2]

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Se llama al metodo del player para detectar colisiones
        #player.collision(cargas)
        # Se llama al metodo del player para actualizar su posicion
        player.update(delta)
        trees1.update(delta)
        trees2.update(delta)
        human.update(delta)
        zombie.update(delta)
        store.update(delta)
        print(human.pos[0])

        lines1.update(delta)
        lines2.update(delta)

        # Se dibuja el grafo de escena principal
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(mainScene, pipeline, "transform")


        # Se dibuja el grafo de escena con texturas
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    mainScene.clear()
    tex_scene.clear()
    
    glfw.terminate()