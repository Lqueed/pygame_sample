import math
import pygame

from cmd.objects.BaseShot import BaseShot
from cmd.config.config import POWER_SHOT_SPEED, POWER_SHOT_IMG
from cmd.helpers.ObjectHelper import rot_center


class PowerShot(BaseShot):
    def __init__(self, id, object_positions, angle, pos_x, pos_y, screen):
        super().__init__(id, object_positions, angle, pos_x, pos_y, screen)
        self.speed = POWER_SHOT_SPEED
        self.set_img(POWER_SHOT_IMG)
        self.power = True
