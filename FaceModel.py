# For use in the wincon check method:
lines_indices = [[0, 3, 1], [3, 6, 1], [6, 9, 1],  # <- Horizontal lines.
                      [0,7,3], [1,8,3], [2,9,3],  # <- Vertical lines.
                      [0,9,4], [2,7,2]]         # <- Diagonals.

class FaceModel:
    def __init__(self):
        self.face_vector = [0, 0, 0,
                            0, 0, 0,
                            0, 0, 0]

    def mark_cell(self, cell_index, content):
        if self.face_vector[cell_index] != 0:
            return False
        self.face_vector[cell_index] = content
        return True

    def rotate_face(self, clockwise):
        """ Rotates a face's surface
        Surface meaning the cells directly on the face, but not the cells from
        faces adjacent to it, which would normally also have to be rotated along
        (e.g., rotating Up should also rotate the upper cells of all faces but
        Down). It is meant to be used only by the turn<a face> methods.
        :param faceVector: The vector representation of the face to rotate.
        :param clockwise: Whether the rotation is clockwise or not.
        :return:
        """

        # Rotating the cells of the chosen face:
        # - save initial values
        ui = self.face_vector[:3]  # initial upper side
        li = self.face_vector[::3]  # initial left side
        di = self.face_vector[6:9]  # initial lower side ("down")
        ri = self.face_vector[2:9:3]  # ...
        cw_factor = 1 if clockwise else -1
        sides = [ui, ri, li, di][::cw_factor]
        # - set final values:
        self.face_vector[2:9:3] = sides[0][::cw_factor]  #
        self.face_vector[6:9] = sides[1][::-cw_factor] # Some sides need to be replaced-in backwards to simulate rotation
        self.face_vector[:3] = sides[2][::-cw_factor]  #
        self.face_vector[::3] = sides[3][::cw_factor]  #

    def check_wincon(self):
        # I should find a clever way to iterate over all useful getter methods instead of using that list but whatevs
        # Unlike with regular Tic-Tac-Toe, ties by double win might occur.
        winners = [False, False]
        for inds in lines_indices:
            line = self.face_vector[inds[0]:inds[1]:inds[2]]
            # Maybe you are thinking "isn't using 1 and 2 too implementation specific and not abstract enough?
            # maybe use parameters for that" and yeah, sure. But also: nah.
            # Actually, how about a global for this?
            winners[0] = (winners[0] or line == [1, 1, 1])
            winners[1] = (winners[1] or line == [2, 2, 2])
        return winners

    def check_if_full(self):
        for cell in self.face_vector:
            if cell == 0:
                return False
        return True

    def get_face_vector(self):
        return self.face_vector

    def get_upper(self, backwards = False):
        backwarder = -1 if backwards else 1
        return self.face_vector[:3][::backwarder]

    def get_equator(self, backwards = False):
        backwarder = -1 if backwards else 1
        return self.face_vector[3:6][::backwarder]

    def get_lower(self, backwards = False):
        backwarder = -1 if backwards else 1
        return self.face_vector[6:9][::backwarder]

    def get_left(self, backwards = False):
        backwarder = -1 if backwards else 1
        return self.face_vector[::3][::backwarder]

    def get_mid(self, backwards = False):
        backwarder = -1 if backwards else 1
        return self.face_vector[1:8:3][::backwarder]

    def get_right(self, backwards = False):
        backwarder = -1 if backwards else 1
        return self.face_vector[2:9:3][::backwarder]

    def get_forward_diagonal(self):
        return self.face_vector[2:4:6]

    def get_back_diagonal(self):
        return self.face_vector[0:4:8]

    def set_face_vector(self, vector):
        self.face_vector = vector

    def set_upper(self, vector):
        self.face_vector[:3] = vector

    def set_equator(self, vector):
        self.face_vector[3:6] = vector

    def set_lower(self, vector):
        self.face_vector[6:9] = vector

    def set_left(self, vector):
        self.face_vector[::3] = vector

    def set_mid(self, vector):
        self.face_vector[1:8:3] = vector

    def set_right(self, vector):
        self.face_vector[2:9:3] = vector