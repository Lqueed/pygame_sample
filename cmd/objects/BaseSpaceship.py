from cmd.helpers.ObjectHelper import rot_center
from cmd.objects.ObjectPositions import ObjectPositions
import pygame
import math


class BaseSpaceship:
    """
    Базовый класс для всех подвижных кораблей - набор методов для всех кораблей
    """
    def __init__(self, screen, object_positions: ObjectPositions, img: str = None):
        self.screen = screen
        self.img = pygame.image.load(img)
        self.orientation = 0
        self.object_positions = object_positions

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

    def get_set_rotation(self, speed, left, right):
        if left:
            self.orientation += 2
        elif right:
            self.orientation -= 2

        if self.orientation >= 360:
            self.orientation = 0
        elif self.orientation <= 0:
            self.orientation = 360

        speed_x = 0
        speed_y = 0
        left = 0
        right = 0
        up = 0
        down = 0
        if speed:
            speed_x = int(math.sin(self.orientation * 0.017) * speed)
            speed_y = int(math.cos(self.orientation * 0.017) * speed)

        if speed_x > 0:
            left = abs(speed_x)
        elif speed_x < 0:
            right = abs(speed_x)
        if speed_y > 0:
            up = abs(speed_y)
        elif speed_y < 0:
            down = abs(speed_y)

        return left, right, up, down