import math
from Auxiliary import *
from Settings import *

# Calculates rotation for when a player explores the cube via left click of the mouse.
class RotationCalculator:
    def __init__(self):
        self.rotating = False
        self.rot_angles = [0.0, 0.0, 0.0]
        self.position_0 = None

    def calculate(self, clickstate):
        if clickstate[0]:
            trigo_y = CUBE_SIDE
            if not self.rotating:
                self.position_0 = mousePos(GAME_WIDTH, GAME_HEIGHT)
                self.rotating = True
            else:
                position_1 = mousePos(GAME_WIDTH, GAME_HEIGHT)
                # Horizontal mov means horizontal rotation applied over the Y axis (ergo, rot_angles[1] = angle on Y)
                self.rot_angles[1] += (math.atan2(self.position_0[0], trigo_y)
                                       - math.atan2(position_1[0], trigo_y)) * ROTATION_MULTIPLIER
                # Vertical rotation is applied on the X axis.
                self.rot_angles[0] += (math.atan2(self.position_0[1], trigo_y)
                                       - math.atan2(position_1[1], trigo_y)) * ROTATION_MULTIPLIER
                self.position_0 = position_1
        else:
            self.rotating = False
            self.rot_angles = [0.0, 0.0, 0.0]

ROT_CALCULATOR = RotationCalculator()
TURNING_ANGLE = 0


# Way drawing all the time except when animating turning one of the cube's faces:
def standard_draw(game_cube):
    # Color all faces that have been marked by the players:
    game_cube.paint_all_marked_faces([[PLAYER_ONE_COLOR], [PLAYER_TWO_COLOR]])
    # Draw the cubes:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPolygonMode(GL_FRONT, GL_FILL)
    glPolygonMode(GL_BACK, GL_FILL)
    game_cube.draw(cExploreRot=True, cAngs=ROT_CALCULATOR.rot_angles, cRot=[1, -1, 0])

    # Draw a wireframe for the Rubik's Cube...
    # maybe instead of coloring and then recoloring each time, have two cubes?
    glPolygonMode(GL_FRONT, GL_LINE)
    glPolygonMode(GL_BACK, GL_LINE)
    game_cube.draw(cRGBL=[black] * 6, cExploreRot=True, cAngs=ROT_CALCULATOR.rot_angles, cRot=[1, -1, 0])


# I could make this set the game_runners phase instead of returning them, but I feel like then the phase
# changing is TOO hidden, so I'm gonna try having the runner itself set its phases first and see how that looks.
def marking_phase(game_runner):
    clickstate = pygame.mouse.get_pressed()
    ROT_CALCULATOR.calculate(clickstate)
    game_cube = game_runner.cube
    next_phase = marking_phase
    # If the cube is not being moved, see if the mouse is over any of the front cells and if so, color that cell blue
    if not ROT_CALCULATOR.rotating:
        ind = mouseOverQ(ZOOMING_FACTOR, CUBE_SIDE, GAME_WIDTH, GAME_HEIGHT, CUBES_OFFSET)
    else:
        ind = None
    # Sets the base colors of the cube (remove this and everything stays black).
    game_cube.setMultiColors(range(26), [egg] * 6, False)
    if ind is not None:
        game_cube.setSingleColors(ind, [blue] + [egg] * 5)

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_SPACE and (ind is not None):
            marked = game_cube.marcar(k=ind, P=game_runner.current_player)
            if marked:
                print "marcado"
                next_phase = turning_phase
            else:
                print MARKED_OVER_MARKED_MESSAGE.format(game_runner.current_player)
        if event.type == QUIT:
            game_runner.running = False
    standard_draw(game_cube)
    return next_phase


def turning_phase(game_runner):
    clickstate = pygame.mouse.get_pressed()
    ROT_CALCULATOR.calculate(clickstate)
    next_phase = turning_phase
    game_cube = game_runner.cube
    game_cube.setMultiColors(range(26), [egg] * 6, False)
    game_model = game_cube.model
    is_clockwise = not clickstate[2]
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_u:
                print "\t Turning Up Face"
                next_phase = animation_phase_generator(game_cube.turn_up, game_model.turn_up, is_clockwise)
            elif event.key == K_l:
                print "\t Turning Left Face"
                next_phase = animation_phase_generator(game_cube.turn_left, game_model.turn_left, is_clockwise)
            elif event.key == K_r:
                print "\t Turning Right Face"
                next_phase = animation_phase_generator(game_cube.turn_right, game_model.turn_right, is_clockwise)
            elif event.key == K_d:
                print "\t Turning Down Face"
                next_phase = animation_phase_generator(game_cube.turn_down,game_model.turn_down, is_clockwise)
            elif event.key == K_f:
                print "\t Turning Front Face"
                next_phase = animation_phase_generator(game_cube.turn_front,game_model.turn_front, is_clockwise)
            elif event.key == K_e:
                print "\t Turning Equator"
                next_phase = animation_phase_generator(game_cube.turn_equator,game_model.turn_equator, is_clockwise)
            elif event.key == K_m:
                print "\t Turning Middle"
                next_phase = animation_phase_generator(game_cube.turn_middle,game_model.turn_middle, is_clockwise)
        if event.type == QUIT:
            game_runner.running = False
    standard_draw(game_cube)
    return next_phase


def animation_phase_generator(turning_method, model_turn_method, is_clockwise):
    # The way I'm using this stuff requires them accepting a game runner argument, which I guess I should change, but eh
    def animation_phase(game_runner):
        global TURNING_ANGLE
        game_cube = game_runner.cube
        game_cube.setMultiColors(range(26), [egg] * 6, False)
        for event in pygame.event.get():
            if event.type == QUIT:
                game_runner.running = False
        if TURNING_ANGLE <= 90:
            game_cube.paint_all_marked_faces([[red], [green]])
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPolygonMode(GL_FRONT, GL_FILL)
            glPolygonMode(GL_BACK, GL_FILL)
            turning_method(TURNING_ANGLE, is_clockwise)

            glPolygonMode(GL_FRONT, GL_LINE)
            glPolygonMode(GL_BACK, GL_LINE)
            turning_method(TURNING_ANGLE, is_clockwise, cRGBL=[black] * 6)

            TURNING_ANGLE += 4.2
            # I think I'm abusing closures here, seriously consider classes yo. How about animating on Rukube instead?
            # And yes, the animation_phase being returned does have the correct turning_method set inside. That's cool.
            return animation_phase
        else:
            model_turn_method(is_clockwise)
            TURNING_ANGLE = 0
            game_cube.paint_all_marked_faces([[red], [green]])
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPolygonMode(GL_FRONT, GL_FILL)
            glPolygonMode(GL_BACK, GL_FILL)
            turning_method(TURNING_ANGLE, is_clockwise)

            glPolygonMode(GL_FRONT, GL_LINE)
            glPolygonMode(GL_BACK, GL_LINE)
            turning_method(TURNING_ANGLE, is_clockwise, cRGBL=[black] * 6)
            return end_a_turn(game_runner)
    return animation_phase
    # TODO: Actually, whatever, I can animate the whole thing inside the one function instead of making Game.py do it.
    # TODO: Also, I should make it better and have a feeling of acceleration rather than just always same velocity.
    # After testing: Yes, definitely need the cool acceleration feel.


def end_a_turn(game_runner):
    game_cube_model = game_runner.cube.model
    next_phase = marking_phase
    # You know, maybe all these functions should just be part of the GameRunner class
    winners = game_cube_model.check_wincons()
    if winners[1] ^ winners[0]:
        winner = 1 if winners[0] else 2
        print WIN_MESSAGE.format(winner, (winner % 2) + 1)
        next_phase = game_over
    elif winners[1] and winners[0]:
        print DOUBLE_WIN_MESSAGE
        next_phase = game_over
    elif game_cube_model.check_if_front_full():
        print OUT_OF_MOVES_MESSAGE
        next_phase = game_over
    else:
        game_runner.change_player()
    return next_phase


def game_over(game_runner):
    clickstate = pygame.mouse.get_pressed()
    ROT_CALCULATOR.calculate(clickstate)
    game_cube = game_runner.cube
    game_cube.setMultiColors(range(26), [egg] * 6, False)
    for event in pygame.event.get():
        if event.type == QUIT:
            game_runner.running = False
    standard_draw(game_cube)
    return game_over
