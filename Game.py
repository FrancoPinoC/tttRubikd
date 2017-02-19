from Rukube import *
from Auxiliary import *
import Settings
import Phases
import Inits


class GameRunner:
    def __init__(self):
        self.current_player = 1
        self.running = True
        self.cube = Rukube(Settings.CUBE_SIDE)
        # self.cube_model SOMEDAY MAYBE I'M GONNA DO IT THIS WAY (but prolly not)
        self.current_phase = Phases.marking_phase

    def run_game(self):
        print Settings.INSTRUCTIONS
        Inits.init_pygame((Settings.GAME_WIDTH, Settings.GAME_HEIGHT), "Tic-Tac-Toe Rubik'd")
        Inits.init_opengl((Settings.GAME_WIDTH, Settings.GAME_HEIGHT), Settings.ZOOMING_FACTOR)
        glLoadIdentity()
        # Look towards the center, from negative Z, with an UP in the Y axis.
        gluLookAt(200.0, 200.0, -2000.0, 0.0, 0.0, 0.0, 0, 1, 0)
        while self.running:
            self.current_phase = self.current_phase(self)
            # Haha, this method is so short now, maybe I *should* actually just move Phases over here to this class.
            pygame.display.flip()
            pygame.time.wait(1000 / 100)
        pygame.quit()
        sys.exit

    def change_player(self):
        self.current_player = self.current_player % 2 + 1
        print Settings.NEW_TURN_MESSAGE.format(self.current_player)


game = GameRunner()
game.run_game()
