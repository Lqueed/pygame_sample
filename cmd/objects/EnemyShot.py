from cmd.objects.BaseShot import BaseShot

from cmd.helpers.ObjectHelper import rot_center
import math
import pygame

from cmd.config.config import SHOT_SPEED, SHOT_IMG


class EnemyShot(BaseShot):
    """
    Базовый класс для выстрелов - хранит состояние, координаты, угол, скорость и id
    """
    def __init__(self, id, object_positions, angle, pos_x, pos_y, screen, shot_speed=SHOT_SPEED):
        super().__init__(id=id,
                         object_positions=object_positions,
                         angle=angle,
                         pos_x=pos_x,
                         pos_y=pos_y,
                         screen=screen,
                         shot_speed=shot_speed)

    def move(self,
             left=None,
             right=None,
             up=None,
             down=None):
        super().move()

        if left:
            self.pos_x += left
        if right:
            self.pos_x -= right
        if up:
            self.pos_y += up
        if down:
            self.pos_y -= down

