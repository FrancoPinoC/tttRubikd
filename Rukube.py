from CubeClass import *
from RukubeModel import *
import math
from Auxiliary import *

offset=6 #separacion extra entre cada cubo (asi no se dibujan muy "pegados")
class Rukube:
    def __init__(self,lado):
        #Hecho de 26 cubos distintos (un cubo en el centro no es necesario)
        cubos=[]
        for i in range(26):
            cubos+=[cubo(0,0,0,0.5)]
        self.cubos=cubos
        self.model = RukubeModel()
        #define escalamiento y posicionamiento de cubos (es el lado de CADA cubo):
        self.lado=lado

        '''caras del Rukube (cada una compuesta de 9 cubos)
         caras comparten cubos con otras caras adyacentes,
         ademas una lista de los cubos que contienen asi como
         un vector con cada casilla de la cara que marcara si
         se ha dubujado en esa casilla o no'''
        #Top
        self.T=[cubos[9],cubos[10],cubos[11],
                cubos[12],cubos[13],cubos[14],
                cubos[0],cubos[1],cubos[2]]
        self.tIndices = [9,10,11,12,13,14,0,1,2]
		#Lista de celdas. El numero indicara si la celda esta pintada o no.
        self.TV=[1,2,0, 0,0,0, 0,0,0]
        #Front
        self.F=[cubos[0],cubos[1],cubos[2],
                cubos[3],cubos[4],cubos[5],
                cubos[6],cubos[7],cubos[8]]
        self.fIndices = [0,1,2,3,4,5,6,7,8]
        self.FV=[0,0,0, 0,0,0, 0,0,0] 
        #Bottom
        self.Bt=[cubos[6],cubos[7],cubos[8],
                 cubos[15],cubos[16],cubos[17],
                 cubos[18],cubos[19],cubos[20]]
        self.btIndices=[6,7,8,15,16,17,18,19,20]
        self.BtV=[0,0,0, 0,0,0, 0,0,0] 
        #Left
        self.L=[cubos[9],cubos[12],cubos[0],
                cubos[21],cubos[22],cubos[3],
                cubos[18],cubos[15],cubos[6]]
        self.lIndices =[9,12,0,21,22,3,18,15,6]
        self.LV=[0,0,0, 0,0,0, 0,0,0] 
        #Right
        self.R=[cubos[2],cubos[14],cubos[11],
                cubos[5],cubos[23],cubos[24],
                cubos[8],cubos[17],cubos[20]]
        self.rIndices=[2,14,11,5,23,24,8,17,20]
        self.RV=[0,0,0, 0,0,0, 0,0,0] 
        #Back
        self.Bck=[cubos[11],cubos[10],cubos[9],
                cubos[24],cubos[25],cubos[21],
                cubos[20],cubos[19],cubos[18]]
        self.bckIndices=[11,10,9,24,25,21,20,19,18]
        self.BckV=[0,0,0, 0,0,0, 0,0,0] 
        #Indices de cubos en la linea zona entre cara frontal y trasera
        self.midIndices=[12,13,14,22,23,15,16,17]
        #Indices de cubos en la linea entre cara izquierda y derecha
        self.zyMidIndices = [1,13,10,4,25,7,16,19]
        #Indices de cubos en la linea entre cara superior e inferior
        self.zxMidIndices = [3,4,5,23,24,25,21,22]
        
    #Fija nuevos colores para algun cubo k
    def setSingleColors(self,k,rgbL):
        self.cubos[k].setColors(rgbL)
    #Fija un color para cada cubo dado, con cada color dado
    # kk es una lista de indices, rgbLL es una lista de listas de 6 colores
    # o una sola lista de seis colores que se usa para todos los cubos (dependiendo de indep)
    def setMultiColors(self,kk,rgbL,indep):
        if indep:
            for i in range(len(kk)):
                self.cubos[kk[i]].setColors(rgbL[i])
        else:
            for i in range(len(kk)):
                self.cubos[kk[i]].setColors(rgbL)

    #Marca una casilla de la cara frontal como pintada
    # k = casilla en la que se dibuja (de 0 a 8), P=jugador que hace marca (1 o 2)
    def marcar(self,k, P):
        self.model.markFront(k,P)
    #Pinta caras dibujadas. Colores es un vector con el color de cada jugador
    #:.... SOMETHINGS WRONG HERE!!
    def paintMarkedFace(self, pColors, faceIndex, face, faceVector):
        k=0
        for i in faceVector:
            if i!=0:
                preColor=face[k].colors
                newColor= preColor[0:faceIndex] + [pColors[i-1]] + preColor[faceIndex+1:]
                #preColor[faceIndex] = pColors[i-1] Can't remember why the above works and this doesn't, but DON'T CHANGE IT
                face[k].setColors(newColor)
            k+=1
    def paintAllMarkedFaces(self, playerColors):
        self.paintMarkedFace(playerColors, 0, self.F, self.model.front)
        self.paintMarkedFace(playerColors, 1, self.L, self.model.left)
        self.paintMarkedFace(playerColors, 2, self.Bck, self.model.back)
        self.paintMarkedFace(playerColors, 3, self.R, self.model.right)
        self.paintMarkedFace(playerColors, 4, self.T, self.model.up)
        self.paintMarkedFace(playerColors, 5, self.Bt, self.model.down)
    ###
    # Use a vector containing representations of the :3, ::3, 6:9 and 2:9:3 indices
    # The vector can be represented with: [[0,3,1],[0,9,3],[6,9,1],[2,9,3]]
    ###
    def rotateFaceAreaV(self, faceVector, clockwise):
        self.model.rotateFaceSurface(faceVector, clockwise)
        # Rotating the cells of the chosen face
        # - save initial values
        #ui = faceVector[:3]  # initial upper side
        #li = faceVector[::3] # initial left side
        #di = faceVector[6:9] # initial lower side ("down")
        #ri = faceVector[2:9:3] #...
        #cwFactor = 1 if clockwise else -1
        #sides = [ui, ri, li, di][::cwFactor]
        # - set final values:
        #faceVector[2:9:3] = sides[0][::cwFactor] #
        #faceVector[6:9] = sides[1][::-cwFactor] # Some sides need to be replaced-in backwards to simulate rotation
        #faceVector[:3] = sides[2][::-cwFactor] #
        #faceVector[::3] = sides[3][::cwFactor]

    def turnFront(self, clockwise=True):
        self.model.turnFront(clockwise)

    def turnUp(self, clockwise=True):
        self.model.turnUp(clockwise)
        # Rotate area of face (the cells on the face itself)
        #self.rotateFaceAreaV(self.TV, clockwise)

        # Rotating lateral sides of the face's cubes (cells corresponding to adjacent faces):
        #fi = self.FV[:3] # initial upper side of the front face
        #li = self.LV[:3] # etc ^-^'...
        #bi = self.BckV[:3]
        #ri = self.RV[:3]
        #cwFactor = 1 if clockwise else -1
        #sides = [bi, ri, li, fi][::cwFactor]
        #self.RV[:3] = sides[0]
        #self.FV[:3] = sides[1]
        #self.BckV[:3] = sides[2]
        #self.LV[:3] = sides[3]
    def turnLeft(self, clockwise=True):
        self.model.turnLeft(clockwise)
        #self.rotateFaceAreaV(self.LV, clockwise)

        #frontsLi = self.FV[::3]
        #upsLi = self.TV[::3]
        #bcksLi = self.BckV[2:9:3][::-1]
        #downsLi = self.BtV[::3]
        #cwFactor = 1 if clockwise else -1
        #sides = [frontsLi, downsLi, upsLi, bcksLi][::cwFactor]
        #self.BtV[::3] = sides[0]
        #self.BckV[2:9:3] = sides[1][::-1]
        #self.FV[::3] = sides[2]
        #self.TV[::3] = sides[3]
    def turnRight(self, clockwise=True):
        self.model.turnRight(clockwise)

    def turnDown(self, clockwise=True):
        self.model.turnDown(clockwise)

    def turnEquator(self, clockwise=True):
        self.model.turnEquator(clockwise)

    def turnMiddle(self, clockwise=True):
        self.model.turnMiddle(clockwise)

    def draw(self, CTpos=[0,0,0,0], cWAng =0, cWRot=None,
        cAngs=[0.0, 0.0, 0.0], cRot=None,cExploreRot=False,cRGBL=None, move=None):
        posFactor = self.lado+offset
        posV = [posFactor+CTpos[0],0+CTpos[1],-posFactor+CTpos[2]]
        #Pinta las caras de acuerdo al color dado (cRGBL es vector de 6 colores)
        if cRGBL!=None:
            for i in range(26):
                self.cubos[i].setColors(cRGBL)
        if cExploreRot and move==None:
            #Dibuja cubos del frente
            for i in range(9):
                self.cubos[i].draw(sz=[self.lado]*3,Tpos=[posV[i%3],posV[i/3],-posFactor],
                                   wAng=cWAng,wRot=cWRot,rot = cRot, angs=cAngs, exploreRot=cExploreRot)
            #Dibuja cubos de atras
            for i in range(9):
                self.cubos[self.bckIndices[i]].draw(sz=[self.lado]*3,Tpos=[(-1)*posV[i%3],posV[i/3],posFactor],
                                   wAng=cWAng,wRot=cWRot,rot = cRot, angs=cAngs, exploreRot=cExploreRot)
            #Cubos restantes
            for i in range(9):
                if i==4: continue #no hay cubo al centro
                if i>4: j=i-1
                else: j=i
                self.cubos[self.midIndices[j]].draw(sz=[self.lado]*3,Tpos=[posV[i%3],posV[i/3],0],
                                   wAng=cWAng,wRot=cWRot,rot = cRot, angs=cAngs, exploreRot=cExploreRot)
        else:
            #Move top
            if move=='t':
                for i in range(9):
                    self.cubos[self.tIndices[i]].draw(sz=[self.lado]*3,Tpos=[posV[i%3],posFactor,posV[i/3]],
					wAng=90,wRot=[0,-1,0])
                for i in range(8):
                    self.cubos[self.zxMidIndices[i]].draw(sz=[self.lado]*3)
                for i in range(9):
                    self.cubos[self.btIndices[i]].draw(sz=[self.lado]*3)
        
        
