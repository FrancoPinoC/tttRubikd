import math
from Auxiliary import *
from Settings import *


class RotationCalculator:
    def __init__(self):
        self.rotating = False
        self.rot_angles = [0.0, 0.0, 0.0]
        self.position_0 = None

    def calculate(self, clickstate):
        if clickstate[0]:
            trigoY = CUBE_SIDE
            if self.rotating == 0:
                self.position_0 = mousePos(GAME_WIDTH, GAME_HEIGHT)
                self.rotating = 1
            else:
                position_1 = mousePos(GAME_WIDTH, GAME_HEIGHT)
                # Horizontal mov means horizontal rotation applied over the Y axis (ergo, rot_angles[1] = angle on Y)
                self.rot_angles[1] += (math.atan2(self.position_0[0], trigoY)
                                       - math.atan2(position_1[0], trigoY)) * ROTATION_MULTIPLIER
                # Vertical rotation is applied on the X axis.
                self.rot_angles[0] += (math.atan2(self.position_0[1], trigoY)
                                       - math.atan2(position_1[1], trigoY)) * ROTATION_MULTIPLIER
                self.position_0 = position_1
        else:
            self.rotating = 0
            self.rot_angles = [0.0, 0.0, 0.0]


# Those two parameters are me, pretending like I'm going to properly separate the logic from the visuals once and for all
def marking_phase(game_cube, game_model, next_phase, calculator):
    clickstate = pygame.mouse.get_pressed()
    calculator.calculate(clickstate)

    # If the cube is not being moved, see if the mouse is over any of the front cells and if so, color that cell blue
    if not calculator.rotating:
        ind = mouseOverQ(ZOOMING_FACTOR, CUBE_SIDE, GAME_WIDTH, GAME_HEIGHT, CUBES_OFFSET)
    else:
        ind = None
    game_cube.setMultiColors(range(26), [egg] * 6, False)
    if ind is not None:
        game_cube.setSingleColors(ind, [blue] + [egg] * 5)

    # TODO: The game itself should be a class. Instance variables could be: Phase, current player. Maybe all of settings?


