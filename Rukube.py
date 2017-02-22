from CubeClass import *
from RukubeModel import *
from Settings import *


class Rukube:
    def __init__(self,lado):
        # Hecho de 26 cubos distintos (un cubo en el centro no es necesario)
        cubos = []
        for i in range(26):
            cubos += [cubo(0, 0, 0, 0.5, egg)]
        self.cubos = cubos
        self.model = RukubeModel()
        # define escalamiento y posicionamiento de cubos (es el lado de CADA cubo):
        self.lado = lado

        '''caras del Rukube (cada una compuesta de 9 cubos)
         caras comparten cubos con otras caras adyacentes,
         ademas una lista de los cubos que contienen asi como
         un vector con cada casilla de la cara que marcara si
         se ha dubujado en esa casilla o no'''
        # Up
        self.U = [cubos[9], cubos[10], cubos[11],
                cubos[12], cubos[13], cubos[14],
                cubos[0], cubos[1], cubos[2]]
        self.u_indices = [0, 1, 2, 12, 13, 14, 9, 10, 11]
		# Lista de celdas. El numero indicara si la celda esta pintada o no.
        self.UV = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # Front
        self.F = [cubos[0],cubos[1],cubos[2],
                cubos[3],cubos[4],cubos[5],
                cubos[6],cubos[7],cubos[8]]
        self.f_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.FV = [0,0,0, 0,0,0, 0,0,0]
        # Down
        self.D = [cubos[6], cubos[7], cubos[8],
                  cubos[15], cubos[16], cubos[17],
                  cubos[18], cubos[19], cubos[20]]
        self.d_Indices = [6, 7, 8, 15, 16, 17, 18, 19, 20]
        self.DV = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # Left
        self.L = [cubos[9],cubos[12],cubos[0],
                cubos[21],cubos[22],cubos[3],
                cubos[18],cubos[15],cubos[6]]
        self.l_indices =[9, 12, 0, 21, 22, 3, 18, 15, 6]
        self.LV = [0,0,0, 0,0,0, 0,0,0]
        # Right
        self.R = [cubos[2],cubos[14],cubos[11],
                cubos[5],cubos[23],cubos[24],
                cubos[8],cubos[17],cubos[20]]
        self.r_indices=[2, 14, 11, 5, 23, 24, 8, 17, 20]
        self.RV = [0,0,0, 0,0,0, 0,0,0]
        # Back
        self.B = [cubos[11], cubos[10], cubos[9],
                  cubos[24], cubos[25], cubos[21],
                  cubos[20], cubos[19], cubos[18]]
        self.b_indices=[11, 10, 9, 24, 25, 21, 20, 19, 18]
        self.BV = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # Indices de cubos en la linea zona entre cara frontal y trasera
        self.standing_indices = [12, 13, 14, 22, 23, 15, 16, 17]
        # Indices de cubos en la linea entre cara izquierda y derecha
        self.mid_indices = [1, 13, 10, 4, 25, 7, 16, 19]
        # Indices de cubos en la linea entre cara superior e inferior
        self.e_indices = [3, 4, 5, 22, 23, 21, 25, 24]
        
    # Fija nuevos colores para algun cubo k
    def setSingleColors(self,k,rgbL):
        self.cubos[k].setColors(rgbL)
    # Fija un color para cada cubo dado, con cada color dado
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
        return self.model.markFront(k,P)

    @staticmethod
    # Pinta caras dibujadas. Colores es un vector con el color de cada jugador
    #:.... SOMETHINGS WRONG HERE!! (past me forgot to mention what this means, it's prolly just about tha comment below)
    def paint_marked_face(p_colors, face_index, face, face_vector):
        k = 0
        for i in face_vector:
            if i != 0:
                pre_color = face[k].colors
                new_color = pre_color[0:face_index] + p_colors[i - 1] + pre_color[face_index + 1:]
                #preColor[faceIndex] = pColors[i-1] Can't remember why the above works and this doesn't, but DON'T CHANGE IT
                face[k].setColors(new_color)
            k += 1

    def paint_all_marked_faces(self, player_colors):
        self.paint_marked_face(player_colors, 0, self.F, self.model.get_face_as_vector('f'))
        self.paint_marked_face(player_colors, 1, self.L, self.model.get_face_as_vector('l'))
        self.paint_marked_face(player_colors, 2, self.B, self.model.get_face_as_vector('b'))
        self.paint_marked_face(player_colors, 3, self.R, self.model.get_face_as_vector('r'))
        self.paint_marked_face(player_colors, 4, self.U, self.model.get_face_as_vector('u'))
        self.paint_marked_face(player_colors, 5, self.D, self.model.get_face_as_vector('d'))

    def turn_front(self, clockwise=True):
        self.model.turn_front(clockwise)

    def turn_up(self, angle, clockwise=True, cRGBL=None):
        pos_factor = self.lado + CUBES_OFFSET
        pos_vector = [pos_factor, 0, -pos_factor]
        clockwise_factor = 1 if clockwise else -1
        if cRGBL is not None:
            for i in range(26):
                self.cubos[i].setColors(cRGBL)

        for i in range(9):
            self.cubos[self.u_indices[i]].draw(sz=[self.lado] * 3, Tpos=[pos_vector[i % 3], pos_factor, -pos_vector[i / 3]],
                                               wAng=angle*clockwise_factor, wRot=[0, -1, 0])
        j = 0
        for i in range(8):
            if i == 4:
                j += 1
            self.cubos[self.e_indices[i]].draw(sz=[self.lado] * 3, Tpos=[pos_vector[j % 3], 0, -pos_vector[j / 3]])
            j += 1
        for i in range(9):
            self.cubos[self.d_Indices[i]].draw(sz=[self.lado] * 3, Tpos=[pos_vector[i % 3], -pos_factor, -pos_vector[i / 3]])
        # self.model.turn_up(clockwise)

    def turn_left(self, clockwise=True):
        self.model.turn_left(clockwise)

    def turn_right(self, clockwise=True):
        self.model.turn_right(clockwise)

    def turn_down(self, clockwise=True):
        self.model.turn_down(clockwise)

    def turn_equator(self, clockwise=True):
        self.model.turn_equator(clockwise)

    def turn_middle(self, clockwise=True):
        self.model.turn_middle(clockwise)

    def draw(self, CTpos=(0,0,0), cWAng =0, cWRot=None,
        cAngs=(0.0, 0.0, 0.0), cRot=None,cExploreRot=False,cRGBL=None, move=None):
        posFactor = self.lado + CUBES_OFFSET
        posV = [posFactor+CTpos[0],0+CTpos[1],-posFactor+CTpos[2]]
        #Pinta las caras de acuerdo al color dado (cRGBL es vector de 6 colores)
        if cRGBL is not None:
            for i in range(26):
                self.cubos[i].setColors(cRGBL)
        if cExploreRot and move is None:
            #Dibuja cubos del frente
            for i in range(9):
                self.cubos[i].draw(sz=[self.lado]*3, Tpos=[posV[i%3], posV[i/3], -posFactor],
                                   wAng=cWAng,wRot=cWRot, rot=cRot, angs=cAngs, exploreRot=cExploreRot)
            #Dibuja cubos de atras
            for i in range(9):
                self.cubos[self.b_indices[i]].draw(sz=[self.lado] * 3, Tpos=[(-1) * posV[i % 3], posV[i / 3], posFactor],
                                                   wAng=cWAng, wRot=cWRot, rot=cRot, angs=cAngs, exploreRot=cExploreRot)
            #Cubos restantes
            for i in range(9):
                if i == 4: continue #no hay cubo al centro
                if i > 4: j = i-1
                else: j = i
                self.cubos[self.standing_indices[j]].draw(sz=[self.lado] * 3, Tpos=[posV[i % 3], posV[i / 3], 0],
                                                          wAng=cWAng, wRot=cWRot, rot=cRot, angs=cAngs, exploreRot=cExploreRot)
        else:
            #Move top
            if move == 't':
                for i in range(9):
                    self.cubos[self.u_indices[i]].draw(sz=[self.lado] * 3, Tpos=[posV[i % 3], posFactor, -posV[i / 3]],
                                                       wAng=45, wRot=[0, -1, 0])
                j = 0
                for i in range(8):
                    if i == 4:
                        j += 1
                    self.cubos[self.e_indices[i]].draw(sz=[self.lado] * 3, Tpos=[posV[j % 3], 0, -posV[j / 3]])
                    j += 1
                for i in range(9):
                    self.cubos[self.d_Indices[i]].draw(sz=[self.lado] * 3, Tpos=[posV[i % 3], -posFactor, -posV[i / 3]])
        
        
