from cmd.helpers.ObjectHelper import rot_center
import pygame


class BaseSpaceship:
    def __init__(self, screen, img: str = None):
        self.screen = screen
        self.img = pygame.image.load(img)
        self.orientation = 0

    def set_ship_img(self, img: str = None):
        self.img = pygame.image.load(img)

    def set_orientation(self, orientation):
        if orientation is not None:
            self.orientation = orientation

    @staticmethod
    def get_orientation(delta_x: int = 0, delta_y: int = 0, changed: bool = False):
        if not changed:
            return None
        if delta_x == 0 and delta_y >= 0:
            return 0
        elif delta_x > 0 and delta_y > 0:
            return 45
        elif delta_x > 0 and delta_y == 0:
            return 90
        elif delta_x > 0 and delta_y < 0:
            return 135
        elif delta_x == 0 and delta_y < 0:
            return 180
        elif delta_x < 0 and delta_y == 0:
            return 270
        elif delta_x < 0 and delta_y < 0:
            return 225
        elif delta_x < 0 and delta_y > 0:
            return 315

    def get_set_orientation(self, delta_x: int = 0, delta_y: int = 0, changed: bool = False):
        orientation = BaseSpaceship.get_orientation(delta_x, delta_y, changed)
        self.set_orientation(orientation)
