from cmd.helpers.ObjectHelper import rot_center
import pygame
import random
from cmd.config.config import (
    RES_X,
    RES_Y,
    BONUS_IMG
)


class BaseBonus:
    """
    Базовый класс для бонусов - хранит состояние, координаты, угол, id и таймер
    """
    def __init__(self, id, object_positions, img, screen, pos_x=0, pos_y=0):
        self.id = id
        self.object_positions = object_positions
        self.img = img
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.abs_pos_x = 0
        self.abs_pos_y = 0
        self.screen = screen
        self.age = 0
        self.set_img(img)
        self.type = 'power'

    def move(self,
             left=None,
             right=None,
             up=None,
             down=None):
        if left:
            self.abs_pos_x += left
            self.pos_x += left
        if right:
            self.abs_pos_x -= right
            self.pos_x -= right
        if up:
            self.abs_pos_y += up
            self.pos_y += up
        if down:
            self.abs_pos_y -= down
            self.pos_y -= down

    def set_img(self, img: str = None):
        self.img = pygame.image.load(img)

    def draw_bonus(self):
        self.screen.blit(self.img,
                         (self.abs_pos_x - 10,
                          self.abs_pos_y - 10))

    def spawn(self):
        self.abs_pos_x = self.pos_x
        self.abs_pos_y = self.pos_y

    def spawn_random(self):
        self.pos_x = random.randint(0, RES_X)
        self.pos_y = random.randint(0, RES_Y)
        self.spawn()