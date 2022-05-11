from cmd.helpers.ObjectHelper import rot_center
from cmd.objects.BaseShot import BaseShot
from BaseSpaceship import BaseSpaceship
from cmd.config.config import (
    RES_X,
    RES_Y,
    EXPLOSION_IMAGE,
    SHOT_BONUS_TIME,
    POWER_SHOT_SPEED,
    POWER_SHOT_IMG,
    SHOT_SPEED,
    SHOT_IMG
)
import pygame
import math


class Player(BaseSpaceship):
    """
    Класс корабля игрока.
    """
    def __init__(self, screen, object_positions, img):
        super().__init__(screen, object_positions, img)
        self.object_positions.set_position('player', RES_X/2, RES_Y/2)
        self.destroyed = False
        self.shot_type = 'base'
        self.double_shot = False
        self.active_bonuses = {}

    def draw(self):
        player_image, new_rect = rot_center(self.img,
                                            self.orientation,
                                            RES_X/2-20,
                                            RES_Y/2-24)
        self.screen.blit(player_image, (RES_X/2-int(new_rect.width/2), RES_Y/2-int(new_rect.height/2)))

    def destroy_player(self):
        self.destroyed = True
        self.set_ship_img(img=EXPLOSION_IMAGE)

    def set_shot_type(self, shot_type: str = 'base'):
        self.shot_type = shot_type
        self.active_bonuses['shot'] = 0

    def set_shot_count(self, double_shot=False):
        self.double_shot = double_shot
        self.active_bonuses['double'] = 0

    def get_shot_type(self):
        return self.shot_type

    def set_bonus(self, bonus_type):
        if bonus_type == 'power':
            self.set_shot_type('power')
        elif bonus_type == 'double':
            self.set_shot_count(True)

    def check_active_bonuses(self):
        to_delete = []
        for bonus_type in self.active_bonuses:
            self.active_bonuses[bonus_type] += 1
            if self.active_bonuses[bonus_type] >= SHOT_BONUS_TIME:
                to_delete.append(bonus_type)
                if bonus_type == 'shot':
                    self.set_shot_type()
                elif bonus_type == 'double':
                    self.set_shot_count()

        for item in to_delete:
            self.active_bonuses.pop(item, False)

    def shoot(self, pos_x, pos_y, shot_id, angle, shot_type):
        if shot_type == 'power':
            shot_speed = POWER_SHOT_SPEED
            shot_img = POWER_SHOT_IMG
            power = True
        else:
            shot_speed = SHOT_SPEED
            shot_img = SHOT_IMG
            power = False

        if self.double_shot:
            shot1_id = f'{shot_id}-1'
            shot2_id = f'{shot_id}-2'

            self.object_positions.shots[shot1_id] = BaseShot(
                id=shot1_id,
                object_positions=self,
                angle=angle,
                pos_x=pos_x + 12 * math.cos(math.radians(angle)),
                pos_y=pos_y - 12 * math.sin(math.radians(angle)),
                screen=self.screen,
                power=power,
                shot_speed=shot_speed,
                shot_img=shot_img
            )

            self.object_positions.shots[shot2_id] = BaseShot(
                id=shot2_id,
                object_positions=self,
                angle=angle,
                pos_x=pos_x - 12 * math.cos(math.radians(angle)),
                pos_y=pos_y + 12 * math.sin(math.radians(angle)),
                screen=self.screen,
                power=power,
                shot_speed=shot_speed,
                shot_img=shot_img
            )
            self.object_positions.shots[shot1_id].draw_shot()
            self.object_positions.shots[shot2_id].draw_shot()
        else:
            self.object_positions.shots[shot_id] = BaseShot(
                id=shot_id,
                object_positions=self,
                angle=angle,
                pos_x=pos_x,
                pos_y=pos_y,
                screen=self.screen,
                power=power,
                shot_speed=shot_speed,
                shot_img=shot_img
            )
            self.object_positions.shots[shot_id].draw_shot()
        self.object_positions.sounds.sound_shot()

