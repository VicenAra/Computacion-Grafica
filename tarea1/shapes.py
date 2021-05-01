import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.ex_curves as cv
import grafica.scene_graph as sg

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape


def createScene(pipeline):

    # Se crean las shapes en GPU
    gpuGreenQuad = createGPUShape(bs.createColorQuad(0.125, 0.705, 0.094), pipeline) # Shape del quad verde
    gpuGrayQuad = createGPUShape(bs.createColorQuad(0.6, 0.6, 0.6), pipeline) # Shape del quad gris
    gpuWhiteQuad = createGPUShape(bs.createColorQuad(1,1,1), pipeline) # Shape del quad blanco


    # Nodo del pasto de la izquierda, quad verde trasladado y escalado
    leftGrassNode = sg.SceneGraphNode("leftGrass")
    leftGrassNode.transform = tr.matmul([tr.translate(-0.85,0,0), tr.scale(0.3,2,1)])
    leftGrassNode.childs = [gpuGreenQuad]

    # Nodo del pasto de la izquierda, quad verde trasladado y escalado
    rightGrassNode = sg.SceneGraphNode("rightGrass")
    rightGrassNode.transform = tr.matmul([tr.translate(0.85,0,0), tr.scale(0.3,2,1)])
    rightGrassNode.childs = [gpuGreenQuad]

    # Nodo que representa el pasto detras de toda la escena
    grassNode = sg.SceneGraphNode("grass")
    grassNode.childs = [leftGrassNode, rightGrassNode]

    # Nodo de la carretera, quad gris escalado y posicionado
    highwayNode = sg.SceneGraphNode("highway")
    highwayNode.transform = tr.matmul([tr.translate(0, 0, 0.2), tr.scale(1.4, 2, 1)])
    highwayNode.childs = [gpuGrayQuad]


    # nodo de la linea de pista derecha, quad blanco escalado y posicionado
    rightLineNode = sg.SceneGraphNode("rightLine")
    rightLineNode.transform = tr.matmul([tr.translate(0.7 , 0, 1), tr.scale(0.03, 2, 1)])
    rightLineNode.childs = [gpuWhiteQuad]

    # nodo de la linea de pista izquierda, quad blanco escalado y posicionado
    leftLineNode = sg.SceneGraphNode("rightLine")
    leftLineNode.transform = tr.matmul([tr.translate(-0.7 , 0, 1), tr.scale(0.03, 2, 1)])
    leftLineNode.childs = [gpuWhiteQuad]

    #nodo que junta ambas lineas de la carretera 
    linesNode = sg.SceneGraphNode("lines")
    linesNode.childs = [leftLineNode, rightLineNode]

    # Nodo del background con todos los nodos anteriores
    backGroundNode = sg.SceneGraphNode("background")
    backGroundNode.childs = [highwayNode, grassNode,linesNode]

    # Nodo padre de la escena
    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [backGroundNode]

    return sceneNode

