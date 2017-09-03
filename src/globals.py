import pygame
from sounds import Sounds, Sound
import getpass
from networking import Networking

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

MAP_WIDTH  = 2500
MAP_HEIGHT = 2500

PORT = 15007

uname = getpass.getuser()

network = Networking()

class Fonts:
    pygame.font.init()
    TITLE = pygame.font.SysFont('Calibri', 25, True, False)
    INFO = pygame.font.SysFont('Calibri', 15, True, False)


sounds = Sounds()
