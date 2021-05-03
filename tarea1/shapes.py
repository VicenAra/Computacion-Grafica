import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.ex_curves as cv
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath

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

    middleLineNode = sg.SceneGraphNode("middleLine")
    middleLineNode.transform = tr.matmul([tr.translate(0, 0, 0.4), tr.scale(0.055, 0.21,1)])
    middleLineNode.childs = [gpuWhiteQuad]

    middleLine1Node = sg.SceneGraphNode("middleLine1")
    middleLine1Node.transform = tr.translate(0,0.8, 0)
    middleLine1Node.childs = [middleLineNode]

    
    middleLine2Node = sg.SceneGraphNode("middleLine2")
    middleLine2Node.transform = tr.translate(0,0.27, 0)
    middleLine2Node.childs = [middleLineNode]

    middleLine3Node = sg.SceneGraphNode("middleLine3")
    middleLine3Node.transform = tr.translate(0,-0.27, 0)
    middleLine3Node.childs = [middleLineNode]

    
    middleLine4Node = sg.SceneGraphNode("middleLine4")
    middleLine4Node.transform = tr.translate(0,-0.8, 0)
    middleLine4Node.childs = [middleLineNode]

    middleLinesNode = sg.SceneGraphNode("middleLines")
    middleLinesNode.childs = [middleLine1Node,middleLine2Node,middleLine3Node,middleLine4Node]
    
    firstMiddleLinesNode = sg.SceneGraphNode("first middleLines")
    firstMiddleLinesNode.childs=[middleLinesNode]

    secondMiddleLinesNode  = sg.SceneGraphNode("second middleLines")
    secondMiddleLinesNode.transform = tr.translate(0, 2.2, 0)
    secondMiddleLinesNode.childs=[middleLinesNode]

    # nodo de la linea de pista derecha, quad blanco escalado y posicionado
    rightLineNode = sg.SceneGraphNode("rightLine")
    rightLineNode.transform = tr.matmul([tr.translate(0.7 , 0, 1), tr.scale(0.02, 2, 1)])
    rightLineNode.childs = [gpuWhiteQuad]

    # nodo de la linea de pista izquierda, quad blanco escalado y posicionado
    leftLineNode = sg.SceneGraphNode("rightLine")
    leftLineNode.transform = tr.matmul([tr.translate(-0.7 , 0, 1), tr.scale(0.02, 2, 1)])
    leftLineNode.childs = [gpuWhiteQuad]


    #nodo que junta ambas lineas de la carretera 
    linesNode = sg.SceneGraphNode("lines")
    linesNode.childs = [leftLineNode, rightLineNode, firstMiddleLinesNode, secondMiddleLinesNode]

    # Nodo del background con todos los nodos anteriores
    backGroundNode = sg.SceneGraphNode("background")
    backGroundNode.childs = [highwayNode, grassNode,linesNode]

    # Nodo padre de la escena
    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [backGroundNode]

    return sceneNode


def createTextureScene(tex_pipeline):

    # Se crean las shapes con texturas en el GPU
    gpuTree = createTextureGPUShape(bs.createTextureQuad(1, 1), tex_pipeline, getAssetPath("tree.png"))

    treeNode = sg.SceneGraphNode("tree")
    treeNode.transform = tr.matmul([tr.scale(0.23, 0.35, 1)])
    treeNode.childs = [gpuTree]

    tree1Node = sg.SceneGraphNode("tree1")
    tree1Node.transform = tr.translate(0,-0.8,0.7)
    tree1Node.childs = [treeNode]

    tree2Node = sg.SceneGraphNode("tree2")
    tree2Node.transform = tr.translate(0, -0.4,0.7)
    tree2Node.childs = [treeNode]

    tree3Node = sg.SceneGraphNode("tree3")
    tree3Node.transform = tr.translate(0, 0, 0.7)
    tree3Node.childs = [treeNode]

    tree4Node = sg.SceneGraphNode("tree4")
    tree4Node.transform = tr.translate(0, 0.4, 0.7)
    tree4Node.childs = [treeNode]

    tree5Node = sg.SceneGraphNode("tree5")
    tree5Node.transform = tr.translate(0, 0.8, 0.7)
    tree5Node.childs = [treeNode]

    treeGroupNode = sg.SceneGraphNode("treeGroup")
    treeGroupNode.childs = [tree1Node, tree2Node, tree3Node, tree4Node, tree5Node]

    leftTreesNode = sg.SceneGraphNode("leftTrees")
    leftTreesNode.transform  =  tr.translate (-0.85,0,0)
    leftTreesNode.childs = [treeGroupNode]
    
    rightTreesNode = sg.SceneGraphNode("righTrees")
    rightTreesNode.transform = tr.translate (0.85, 0 ,0)
    rightTreesNode.childs = [treeGroupNode]
    
    leftUpperTreesNode = sg.SceneGraphNode("leftUpper")
    leftUpperTreesNode.transform = tr.translate(-0.85, 2, 0)
    leftUpperTreesNode.childs = [treeGroupNode]

    rightUpperTreesNode = sg.SceneGraphNode("rightUpper")
    rightUpperTreesNode.transform = tr.translate(0.85, 2, 0)
    rightUpperTreesNode.childs = [treeGroupNode]
    
    treesSceneNode =sg.SceneGraphNode("trees")
    treesSceneNode.childs = [leftTreesNode,rightTreesNode,rightUpperTreesNode,leftUpperTreesNode]

    firstTreesSceneNode = sg.SceneGraphNode("first trees")
    firstTreesSceneNode.childs =[treesSceneNode]

    secondTreesSceneNode = sg.SceneGraphNode("second trees")
    secondTreesSceneNode.transform = tr.translate(0, 4, 0)
    secondTreesSceneNode.childs = [treesSceneNode]

    textureSceneNode = sg.SceneGraphNode("worldTextures")
    textureSceneNode.childs = [firstTreesSceneNode,secondTreesSceneNode]


    return textureSceneNode   
