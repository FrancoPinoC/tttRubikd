linesIndices = [[0,3,1],[3,6,1],[6,9,1],  # <- Horizontal lines.
                      [0,7,3],[1,8,3],[2,9,3],  # <- Vertical lines.
                      [0,9,4], [2,7,2]]         # <- Diagonals.

linesD = {'up' : [0,3,1], 'equator' : [3,6,1], 'down' : [6,9,1],
             'left' : [0,7,3], 'middle' : [1,8,3], 'right' : [2,9,3],
             'forwardDiagonal' : [0,9,4], 'backDiagonal' : [2,7,2]}

# Names are chosen (mostly) using the "Singmaster notation" with MES extension.
# (how cool of a name is "Singmaster" btw, like daamn)
# TODO: Abstract from turn[Direction] methods (having one for each possible turn feels dumb).
from FaceModel import *

class RukubeModel:
    def __init__(self):
        self.front = FaceModel()
        self.left = FaceModel()
        self.back = FaceModel()
        self.right = FaceModel()
        self.up = FaceModel()
        self.down = FaceModel()

        self.faces_dict = {'f': self.front, 'l': self.left, 'b': self.back,
                           'r': self.right, 'u': self.up, 'd': self.down}
        # (A face should maybe be an object of its own?). OK past me, done.

    def get_face_as_vector(self, face_name):
        return self.faces_dict[face_name].get_face_vector()

    def getAllFaces(self):
        return [self.front, self.left, self.back, self.right, self.up, self.down]

    def markFront(self, cellIndex, content):
        """ Marks a cell of the front face with whatever the content is

        :param cellIndex: Should be a number from 0 to 9.
        :param content: Should probably be 1 or 2.
        :return:
        """
        self.front.mark_cell(cellIndex, content)

    def rotateFaceSurface(self, faceVector, clockwise):
        """ Rotates a face's surface

        Surface meaning the cells directly on the face, but not the cells from
        faces adjacent to it, which would normally also have to be rotated along
        (e.g., rotating Up should also rotate the upper cells of all faces but
        Down). It is meant to be used only by the turn<a face> methods.
        :param faceVector: The vector representation of the face to rotate.
        :param clockwise: Whether the rotation is clockwise or not.
        :return:
        """
        if(faceVector == self.front):
            self.front.rotate_face(clockwise)
        # Rotating the cells of the chosen face:
        # - save initial values
        ui = faceVector[:3]  # initial upper side
        li = faceVector[::3] # initial left side
        di = faceVector[6:9] # initial lower side ("down")
        ri = faceVector[2:9:3] #...
        cwFactor = 1 if clockwise else -1
        sides = [ui, ri, li, di][::cwFactor]
        # - set final values:
        faceVector[2:9:3] = sides[0][::cwFactor] #
        faceVector[6:9] = sides[1][::-cwFactor] # Some sides need to be replaced-in backwards to simulate rotation
        faceVector[:3] = sides[2][::-cwFactor] #
        faceVector[::3] = sides[3][::cwFactor] #

    def turnUp(self, clockwise=True):
        """
        Does a quarter turn of the Up face.
        :param clockwise: Whether the turn is clockwise or not (when looking directly at the face)
        :return:
        """
        self.up.rotate_face(clockwise)

        # Rotating lateral sides of the face's cubes (cells corresponding to adjacent faces):
        # fi = self.front[:3] # initial upper side of the front face
        f_upper = self.front.get_upper()
        l_upper = self.left.get_upper() # etc ^-^'...
        b_upper = self.back.get_upper()
        r_upper = self.right.get_upper()
        cwFactor = 1 if clockwise else -1
        sides = [b_upper, r_upper, l_upper, f_upper][::cwFactor]
        self.right.set_upper(sides[0])
        # self.front[:3] = sides[1]
        self.front.set_upper(sides[1])
        self.back.set_upper(sides[2])
        self.left.set_upper(sides[3])

    def turnDown(self, clockwise=True):
        self.down.rotate_face(clockwise)
        front_low = self.front.get_lower()
        left_low = self.left.get_lower()
        back_low = self.back.get_lower()
        right_low = self.right.get_lower()
        cwFactor = -1 if clockwise else 1
        sides = [back_low, right_low, left_low, front_low][::cwFactor]
        self.right.set_lower(sides[0])
        self.front.set_lower(sides[1])
        self.back.set_lower(sides[2])
        self.left.set_lower(sides[3])

    def turnLeft(self, clockwise=True):

        self.left.rotate_face(clockwise)
        # Parts from other faces corresponding to sides that touch the left face:
        fronts_left = self.front.get_left()
        # Clockwise movement => down's left side goes up to the back side. Get it backwards to preserve orientation
        ups_left = self.up.get_left(backwards=not clockwise)
        bcks_right = self.back.get_right(backwards=True)
        downs_left = self.down.get_left(backwards=clockwise)

        cwFactor = 1 if clockwise else -1
        sides = [fronts_left, downs_left, ups_left, bcks_right][::cwFactor]
        self.down.set_left(sides[0])
        self.back.set_right(sides[1])
        self.front.set_left(sides[2])
        self.up.set_left(sides[3])

    def turnRight(self, clockwise=True):
        self.right.rotate_face(clockwise)
        # Parts from other faces corresponding to sides that touch the right face:
        fronts_right = self.front.get_right()
        ups_right = self.up.get_right(backwards=clockwise)
        bcks_left = self.back.get_left(backwards=True)
        downs_right = self.down.get_right(backwards=not clockwise)

        cwFactor = -1 if clockwise else 1
        sides = [fronts_right, downs_right, ups_right, bcks_left][::cwFactor]
        self.down.set_right(sides[0])
        self.back.set_left(sides[1])
        self.front.set_right(sides[2])
        self.up.set_right(sides[3])

    def turnFront(self, clockwise=True):
        self.front.rotate_face(clockwise)

        ups_lower = self.up.get_lower(backwards=clockwise)
        lefts_right = self.left.get_right(backwards=not clockwise)
        rights_left = self.right.get_left(backwards=not clockwise)
        downs_upper = self.down.get_upper(backwards=clockwise)

        cw_factor = 1 if clockwise else -1
        sides = [ups_lower, lefts_right, rights_left, downs_upper][::cw_factor]
        self.right.set_left(sides[0])
        self.up.set_lower(sides[1])
        self.down.set_upper(sides[2])
        self.left.set_right(sides[3])

    def turnEquator(self, clockwise=True):
        # Direction is as in the Down face.
        frontsEi = self.front.get_equator()
        leftsEi = self.left.get_equator()
        rightsEi = self.right.get_equator()
        backsEi = self.back.get_equator()

        cwFactor = -1 if clockwise else 1
        sides = [backsEi, rightsEi, leftsEi, frontsEi][::cwFactor]
        self.right.set_equator(sides[0])
        self.front.set_equator(sides[1])
        self.back.set_equator(sides[2])
        self.left.set_equator(sides[3])

    def turnMiddle(self, clockwise=True):
        # Direction as Left face.
        frontsMi = self.front.get_mid()
        upsMi = self.up.get_mid(backwards=not clockwise)
        bcksMi = self.back.get_mid(backwards=True)
        downsMi = self.down.get_mid(backwards=clockwise)

        cwFactor = 1 if clockwise else -1
        sides = [frontsMi, downsMi, upsMi, bcksMi][::cwFactor]
        self.down.set_mid(sides[0])
        self.back.set_mid(sides[1])
        self.front.set_mid(sides[2])
        self.up.set_mid(sides[3])

    def checkWinConsAt(self, face):
        # Unlike with regular Tic-Tac-Toe, ties by double win might occur.
        winners = [False, False]
        for inds in linesIndices:
            line = face[inds[0]:inds[1]:inds[2]]
            winners[0] = (winners[0] or line == [1,1,1])
            winners[1] = (winners[1] or line == [2,2,2])
        return winners

    def check_if_full(self, face):
        for n in face:
            if n == 0:
                return False
        return True
