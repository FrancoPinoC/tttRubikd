linesIndices = [[0,3,1],[3,6,1],[6,9,1],  # <- Horizontal lines.
                      [0,7,3],[1,8,3],[2,9,3],  # <- Vertical lines.
                      [0,9,4], [2,7,2]]         # <- Diagonals.
linesD = {'up' : [0,3,1], 'equator' : [3,6,1], 'down' : [6,9,1],
             'left' : [0,7,3], 'middle' : [1,8,3], 'right' : [2,9,3],
             'forwardDiagonal' : [0,9,4], 'backDiagonal' : [2,7,2]}
# Names are chosen (mostly) using the "Singmaster notation" with MES extension.
# TODO: Abstract from turn[Direction] methods (having one for each possible turn feels dumb).
class RukubeModel:
    def __init__(self):
        self.front = [0,0,0, 0,0,0, 0,0,0]
        self.left = [0]*9
        self.back = [0]*9
        self.right = [0]*9
        self.up = [0]*9
        self.down = [0]*9
        # (A face should maybe be an object of its own?)

    def getAllFaces(self):
        return [self.front, self.left, self.back, self.right, self.up, self.down]

    def markFront(self, cellIndex, content):
        """ Marks a cell of the front face with whatever the content is

        :param cellIndex: Should be a number from 0 to 9.
        :param content: Should probably be 1 or 2.
        :return:
        """
        self.front[cellIndex] = content

    def rotateFaceSurface(self, faceVector, clockwise):
        """ Rotates a face's surface

        Surface meaning the cells directly on the face, but not the cells from
        faces adjacent to it, which would normally also have to be rotated along
        (e.g., rotating Up should also rotate the upper cells of all faces but
        Down). It is meant to be used only by the turn<a face> method.
        :param faceVector: The vector representation of the face to rotate.
        :param clockwise: Whether the rotation is clockwise or not.
        :return:
        """

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
        self.rotateFaceSurface(self.up, clockwise)

        # Rotating lateral sides of the face's cubes (cells corresponding to adjacent faces):
        fi = self.front[:3] # initial upper side of the front face
        li = self.left[:3] # etc ^-^'...
        bi = self.back[:3]
        ri = self.right[:3]
        cwFactor = 1 if clockwise else -1
        sides = [bi, ri, li, fi][::cwFactor]
        self.right[:3] = sides[0]
        self.front[:3] = sides[1]
        self.back[:3] = sides[2]
        self.left[:3] = sides[3]
    def turnDown(self, clockwise=True):
        self.rotateFaceSurface(self.down, clockwise)
        frontsDi = self.front[6:9]
        leftsDi = self.left[6:9]
        backsDi = self.back[6:9]
        rightsDi = self.right[6:9]
        cwFactor = -1 if clockwise else 1
        sides = [backsDi, rightsDi, leftsDi, frontsDi][::cwFactor]
        self.right[6:9] = sides[0]
        self.front[6:9] = sides[1]
        self.back[6:9] = sides[2]
        self.left[6:9] = sides[3]

    def turnLeft(self, clockwise=True):

        self.rotateFaceSurface(self.left, clockwise)
        # Parts from other faces corresponding to sides that touch the left face:
        frontsLi = self.front[::3]
        upsLi = self.up[::3]
        bcksLi = self.back[2:9:3][::-1]
        downsLi = self.down[::3]

        cwFactor = 1 if clockwise else -1
        sides = [frontsLi, downsLi, upsLi, bcksLi][::cwFactor]
        self.down[::3] = sides[0]
        self.back[2:9:3] = sides[1][::-1]
        self.front[::3] = sides[2]
        self.up[::3] = sides[3]

    def turnRight(self, clockwise=True):
        self.rotateFaceSurface(self.right, clockwise)
        # Parts from other faces corresponding to sides that touch the right face:
        frontsRi = self.front[2:9:3]
        upsRi = self.up[2:9:3]
        bcksRi = self.back[::3][::-1]
        downsRi = self.down[2:9:3]

        cwFactor = -1 if clockwise else 1
        sides = [frontsRi, downsRi, upsRi, bcksRi][::cwFactor]
        self.down[2:9:3] = sides[0]
        self.back[::3] = sides[1][::-1]
        self.front[2:9:3] = sides[2]
        self.up[2:9:3] = sides[3]

    def turnFront(self, clockwise=True):
        self.rotateFaceSurface(self.front, clockwise)

        upsDi = self.up[6:9]
        leftsRi = self.left[2:9:3]
        rightsLi = self.right[::3]
        downsUi = self.down[:3]

        cwFactor = 1 if clockwise else -1
        sides = [upsDi, leftsRi, rightsLi, downsUi][::cwFactor]
        self.right[::3] = sides[0][::cwFactor]
        self.up[6:9] = sides[1][::-cwFactor]
        self.down[:3] = sides[2][::-cwFactor]
        self.left[2:9:3] = sides[3][::cwFactor]

    def turnEquator(self, clockwise=True):
        # Direction is as in the Down face.
        frontsEi = self.front[3:6]
        leftsEi = self.left[3:6]
        rightsEi = self.right[3:6]
        backsEi = self.back[3:6]

        cwFactor = -1 if clockwise else 1
        sides = [backsEi, rightsEi, leftsEi, frontsEi][::cwFactor]
        self.right[3:6] = sides[0]
        self.front[3:6] = sides[1]
        self.back[3:6] = sides[2]
        self.left[3:6] = sides[3]

    def turnMiddle(self, clockwise=True):
        # Direction as Left face.
        frontsMi = self.front[1:8:3]
        upsMi = self.up[1:8:3]
        bcksMi = self.back[1:8:3][::-1]
        downsMi = self.down[1:8:3]

        cwFactor = 1 if clockwise else -1
        sides = [frontsMi, downsMi, upsMi, bcksMi][::cwFactor]
        self.down[1:8:3] = sides[0]
        self.back[1:8:3] = sides[1][::-1]
        self.front[1:8:3] = sides[2]
        self.up[1:8:3] = sides[3]

    def checkWinConsAt(self, face):
        # Unlike with regular Tic-Tac-Toe, ties by double win might occur.
        winners = [False, False]
        for inds in linesIndices:
            line = face[inds[0]:inds[1]:inds[2]]
            winners[0] = (winners[0] or line==[1,1,1])
            winners[1] = (winners[1] or line==[2,2,2])
        return winners

    def checkIfFull(self, face):
        for n in face:
            if n == 0:
                return False
        return True
