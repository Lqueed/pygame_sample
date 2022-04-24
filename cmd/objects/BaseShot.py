from cmd.helpers.ObjectHelper import rot_center
import math
import pygame

from cmd.config.config import SHOT_SPEED, SHOT_IMG


class BaseShot:
    """
    Базовый класс для выстрелов - хранит состояние, координаты, угол, скорость и id
    """
    def __init__(self, id, object_positions, angle, pos_x, pos_y, screen):
        self.id = id
        self.img = None
        self.object_positions = object_positions
        self.angle = angle
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.screen = screen
        self.speed = SHOT_SPEED
        self.age = 0
        self.set_img(SHOT_IMG)
        self.power = False

    def set_img(self, img):
        self.img = pygame.image.load(img)
        rotated_shot, _ = rot_center(self.img, self.angle, self.pos_x, self.pos_y)
        self.img = rotated_shot

    def move(self):
        """
        Летит строго туда куда запустили, храним угол и скорость
        """
        speed_x = int(math.sin(self.angle * 0.017) * self.speed)
        speed_y = int(math.cos(self.angle * 0.017) * self.speed)

        left = None
        right = None
        up = None
        down = None
        if speed_x > 0:
            left = abs(speed_x)
        elif speed_x < 0:
            right = abs(speed_x)
        if speed_y > 0:
            up = abs(speed_y)
        elif speed_y < 0:
            down = abs(speed_y)

        if left:
            self.pos_x -= left
        if right:
            self.pos_x += right
        if up:
            self.pos_y -= up
        if down:
            self.pos_y += down

        self.age += 1

    def draw_shot(self):
        self.screen.blit(self.img, (self.pos_x, self.pos_y))