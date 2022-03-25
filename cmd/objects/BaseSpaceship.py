from cmd.helpers.ObjectHelper import rot_center
import pygame
import math


class BaseSpaceship:
    """
    Базовый класс для всех подвижных кораблей - набор методов для всех кораблей
    """
    def __init__(self, screen, object_positions, img: str = None):
        self.screen = screen
        self.img = pygame.image.load(img)
        self.orientation = 0
        self.object_positions = object_positions
        self.prev_direction = (0, 0, 0, 0)

    def set_ship_img(self, img: str = None):
        self.img = pygame.image.load(img)

    def set_orientation(self, orientation):
        if orientation is not None:
            self.orientation = orientation

    def rotate(self, left, right):
        if left:
            self.orientation += 2
        elif right:
            self.orientation -= 2

        if self.orientation >= 360:
            self.orientation = 0
        elif self.orientation <= 0:
            self.orientation = 360

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

    def get_set_rotation(self, speed, left, right, destroyed: bool = False):
        if destroyed:
            return 0, 0, 0, 0

        self.rotate(left, right)

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

        self.prev_direction = (left, right, up, down)

        return left, right, up, down

    def get_set_rotation_free_flight(self, left, right):
        self.rotate(left, right)
        return self.prev_direction
