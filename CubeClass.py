import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Auxiliary import *

#Fnc auxiliar para formar vertices de caras del cubo
def set4Vert(vertList):
	for v in vertList:
		glVertex3fv(v)


	
class cubo:
	def __init__(self, xc,yc,zc,mitad_cara):
                #posicion central del cubo
                '''^no afecta eleccion de vertices, pues las variables de posicion
                solo se usaran para guardar las traslaciones del objeto y para poder
                obtener luego la posicion del cubo'''
		self.x = xc
		self.y = yc
		self.z = zc
		
		#Vertices del cubo:
		self.a = [-mitad_cara,-mitad_cara,-mitad_cara]
		self.b = [mitad_cara,-mitad_cara,-mitad_cara]
		self.c = [mitad_cara,mitad_cara,-mitad_cara]
		self.d = [-mitad_cara,mitad_cara,-mitad_cara]
		self.e = [-mitad_cara,-mitad_cara,mitad_cara]
		self.f = [mitad_cara,-mitad_cara,mitad_cara]
		self.g = [mitad_cara,mitad_cara,mitad_cara]
		self.h = [-mitad_cara,mitad_cara,mitad_cara]

                #Color de las caras del cubo, por default son de color 'egg'
		self.colors=[egg]*6

		#Caras del cubo:
		self.l = glGenLists(1)
		glNewList(self.l,GL_COMPILE)
		
		glBegin(GL_QUADS)
		glColor4fv(egg)
		set4Vert([self.a,self.b,self.c,self.d])
		set4Vert([self.b,self.f,self.g,self.c])
		set4Vert([self.f,self.e,self.h,self.g])
		set4Vert([self.e,self.a,self.d,self.h])
		set4Vert([self.d,self.c,self.g,self.h])
		set4Vert([self.a,self.e,self.f,self.b])
		
		glEnd()
		glEndList()
		
	#Rehace caras, fijando nuevos colores para cada una.
        #rgbL debe ser una lista de seis colores.
        '''(inicialmente) El primer color de la lista se dibuja en lado frontal del cubo,
        el segundo en la cara izquierda, el tercero en la cara trasera, el cuarto en
        la cara derecha, el quinto en la cara superior y el sexto en la cara inferior
        ( cubeColors=(front, L, back, R, top, bottom) )'''
	def setColors(self,rgbL):
		self.l = glGenLists(1)
		glNewList(self.l,GL_COMPILE)
		
		glBegin(GL_QUADS)
		
		glColor4fv(rgbL[0])
		set4Vert([self.a,self.b,self.c,self.d])
		
		glColor4fv(rgbL[1])
		set4Vert([self.b,self.f,self.g,self.c])
		
		glColor4fv(rgbL[2])
		set4Vert([self.f,self.e,self.h,self.g])
		
		glColor4fv(rgbL[3])
		set4Vert([self.e,self.a,self.d,self.h])
		
		glColor4fv(rgbL[4])
		set4Vert([self.d,self.c,self.g,self.h])
		
		glColor4fv(rgbL[5])
		set4Vert([self.a,self.e,self.f,self.b])
		
		glEnd()
		glEndList()
		self.colors=rgbL
	#Metodo de dibujo (y transformacion) del cubo.
	def draw(self,sz=None, Tpos=[0,0,0,0], wAng =0, wRot=None,
                 angs=[0.0, 0.0, 0.0], rot=None,RGBL=None,exploreRot=False):
                if RGBL!=None:
                        self.setColors(RGBL)
		glPushMatrix()
		if Tpos!=[0,0,0,0]:
			self.x=Tpos[0]
			self.y=Tpos[1]
			self.z=Tpos[2]
		#Rotacion alrededor del centro del sistema de coordenadas externo
                 #Todos los ejes giran en el mismo angulo
		 #( "el giro alrededor del sol, en un sistema solar")
                rotAux=[0.0,0.0,0.0]
		if rot!=None and exploreRot:
                        for i in range(3):
                                if (rot[i]!=0):
                                        rotAux[i]=rot[i]
                                        rotAux[(i+1)%3]=0.0
                                        rotAux[(i+2)%3]=0.0
                                        glRotate(angs[i],rotAux[0],rotAux[1],rotAux[2])
                        #ExploreRot decide si se gira en todos los angulos de forma independiente
                        # o si es solo un giro de un solo eje (o giro de un solo angulo)
                else:
                        if wRot!=None:
                                glRotate(wAng, wRot[0],wRot[1],wRot[2])
		glTranslatef(self.x,self.y,self.z)
		if (sz!=None):
			glScalef(sz[0],sz[1],sz[2])
			
		#Rotacion de angulos independentes, en ejes centrados en objeto
                 #("rotacion del planeta sobre si mismo")
		if rot!=None and not exploreRot:
                        for i in range(3):
                                if (rot[i]!=0):
                                        rotAux[i]=rot[i]
                                        rotAux[(i+1)%3]=0.0
                                        rotAux[(i+2)%3]=0.0
                                        glRotate(angs[i],rotAux[0],rotAux[1],rotAux[2])
		#Rot aux deja solo un eje con "1" o "-1", que es el eje correspondiente al angulo angs[i]
		glCallList(self.l)
		
		glPopMatrix()
