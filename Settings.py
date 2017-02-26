# Zooming factor. The smaller it is, the bigger the modeled object looks.
ZOOMING_FACTOR = 1.6

GAME_WIDTH = 700
GAME_HEIGHT = 700

# Rotation multiplier. When exploring the cube via left-click, this define how fast the cube moves in relation to the
# mouse's movement. For the same distance traveled by the cursor: The bigger the multiplier, the faster the cube rotates
ROTATION_MULTIPLIER = 130

CUBE_SIDE = 200
# Extra separation between cubes, so as not to draw them too close together
CUBES_OFFSET = 5

# Colors
red = [0.9, 0.0, 0.0, 1]
green = [0.0, 0.9, 0.0, 1]
blue = [0.0, 0.0, 0.9, 1]
cyan = [0.0, 1.0, 1.0, 1]
ylw = [1.0, 1.0, 0.0, 1]
prpl = [0.7, 0.0, 0.8, 1]
orng = [1.0, 0.5, 0.0, 1]
black = [0.0, 0.0, 0.0, 1]
white = [1.0, 1.0, 1.0, 1]
grey = [0.5, 0.5, 0.5, 1]
egg = [0.95, 0.95, 0.95, 1]
#########################

PLAYER_ONE_COLOR = red
PLAYER_TWO_COLOR = green
PLAYER_ONE_BG = [1.0, 0.9, 0.9, 1.0]
PLAYER_TWO_BG = [0.8, 1.0, 0.7, 1.0]
NEW_TURN_MESSAGE = "It's Player {0}'s turn!\n" \
                   "\tMark one of the avilable spaces now"
MARKED_OVER_MARKED_MESSAGE = "\tYou tried to mark over an already marked spot Player {0}... try again"
CORRECT_MARK_MESSAGE = "\tMarked a space. Turn one of the cubes faces now!"
WIN_MESSAGE = "\nWOOOOO, PLAYER {0} WON! \n Suck it, Player {1}"
DOUBLE_WIN_MESSAGE = "\nYOU BOTH WON! ...? ... I mean, I don't know, is that good? D-Do you feel good about that?"
OUT_OF_MOVES_MESSAGE = "\nSo the whole front face is full... um... NOBODY WON, WOO \\o/!"

INSTRUCTIONS = "- Click and drag to rotate the whole cube around during the marking phase.\n" \
                 "- Hover your mouse over the cell you want to mark,\n" \
                 "  then press the spacebar to do so. P1 is red, P2 is green.\n" \
                 "- How to rotate individual faces \n" \
                 "   f: Front face (the one that faces you when the cube is still)\n" \
                 "   r: Right\n" \
                 "   l: Left\n" \
                 "   d: Down\n" \
                 "   u: Up\n" \
                 "   e: Equator (horizontal line)\n" \
                 "   m: Middle (vertical line)\n" \
                 "  All horizontal and all vertical sides rotate in the same direction.\n" \
                 "  Clockwise according to the upper face for horizontal, and clockwise\n" \
                 "  according to the left face for all vertical sides.\n" \
                 "  Right click while pressing the buttons to make it counterclockwise.\n" \
                 "(this is an unfinished demo).\n" \
                 "******************************\n"
