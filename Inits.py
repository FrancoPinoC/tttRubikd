import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
def init_pygame((w,h), title=""):
    pygame.init()
    pygame.display.set_mode((w,h), OPENGL|DOUBLEBUF)
    pygame.display.set_caption(title)

def init_opengl((w,h),zoomK):
    reshape((w,h),zoomK)
    init()
 
def init():
    # setea el color de fondo
    glClearColor(1.0, 1.0, 1.0, 1.0)
	
    # se habilitan las transparencias
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # el color debe incluir la cuarta componente, alpha
    # alpha=1  --> objeto totalmente opaco
    # alpha=0  --> opbjeto totalmente transparente

    glShadeModel(GL_SMOOTH)
 
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
	
def reshape((width, height), zoomK): #zoomK define la "ampliacion" con la que se dibuja en 3D
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluPerspective(60.0, float(width)/float(height), 0.1, 20000.0)
    glOrtho(-zoomK*width,zoomK*width,-zoomK*height,zoomK*height,-1,50000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
