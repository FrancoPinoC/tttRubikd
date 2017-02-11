''' Utilidades varias '''

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


#mousePos: Facilita la obtencion de una version mas manejable de la
 #posicion del mouse, que no sea tupla (inmutables) y que este en el
 #en un sistema de coordenadas coherente con el usado para el cubo (centrado
 #en el centro de la pantalla)

def mousePos(wid,hei):
        pos = pygame.mouse.get_pos()
        pos = [pos[0], pos[1]] #boo tuples <.<
        pos[0] -= wid/2
        pos[1] -= hei/2
        return pos


#Deteccion de mouse sobre cubos:
    #Retorna el indice del cubo sobre el que esta el mouse (None si ninguno)
    #(asume cubo centrado en origen, de otro modo, se puede manejar el sistema
    # del mouse con las variables wi y he)
def mouseOverQ(zmK, lado, wi, he, off):
    mPos = mousePos(wi, he)
    # Si el mouse no esta en el rango del cubo
    if (abs(mPos[0]) > 3.0*(lado+off)/(zmK*4)) and (abs(mPos[1]) > 3.0*(lado+off)/(zmK*4)):
        return None
    # Si esta sobre el cubo 4 (centro)
    elif (abs(mPos[0]) <= (lado+off)/(zmK*4.0)) and (abs(mPos[1]) <= (lado+off)/(zmK*4.0)):
        return 4
    # Si sobre 3 (centro izquierda)
    elif (abs(mPos[1]) <= (lado+off)/(zmK*4.0)) and \
         (abs(mPos[0]+2.0*(lado+off)/(zmK*4))<=(lado+off)/(zmK*4.0)):
        return 3
    # Si sobre 5 (centro derecha)
    elif (abs(mPos[1]) <= (lado+off)/(zmK*4.0)) and \
         (abs(mPos[0]-2.0*(lado+off)/(zmK*4)) <= (lado+off)/(zmK*4.0)):
        return 5
    # Si sobre 0 (esquina izq superior)
    elif (abs(mPos[1]+2.0*(lado+off)/(zmK*4))) <= (lado+off)/(zmK*4.0) and \
         (abs(mPos[0]+2.0*(lado+off)/(zmK*4)) <= (lado+off)/(zmK*4.0)):
        return 0
    # Sobre 1 (centro superior)
    elif (abs(mPos[0]) <= (lado+off)/(zmK*4.0)) and \
         (abs(mPos[1]+2.0*(lado+off)/(zmK*4)) <= (lado+off)/(zmK*4.0)):
        return 1
    # Sobre 2 (esquina der superior)
    elif (abs(mPos[0]-2.0*(lado+off)/(zmK*4))) <= (lado+off)/(zmK*4.0) and \
         (abs(mPos[1]+2.0*(lado+off)/(zmK*4)) <= (lado+off)/(zmK*4.0)):
        return 2
    # Sobre 6 (esquina inferior izq)
    elif (abs(mPos[0]+2.0*(lado+off)/(zmK*4))) <= (lado+off)/(zmK*4.0) and \
         (abs(mPos[1]-2.0*(lado+off)/(zmK*4)) <= (lado+off)/(zmK*4.0)):
        return 6
    # Sobre 7 (centro inferior)
    elif (abs(mPos[0]) <= (lado+off)/(zmK*4.0)) and \
         (abs(mPos[1]-2.0*(lado+off)/(zmK*4))<=(lado+off)/(zmK*4.0)):
        return 7
    # Sobre 8 (esquina inf der)
    elif (abs(mPos[0]-2.0*(lado+off)/(zmK*4))) <= (lado+off)/(zmK*4.0) and \
         (abs(mPos[1]-2.0*(lado+off)/(zmK*4)) <= (lado+off)/(zmK*4.0)):
        return 8
