from cmd.helpers.ObjectHelper import rot_center
from BaseSpaceship import BaseSpaceship
from cmd.config.config import (
    RES_X,
    RES_Y,
    EXPLOSION_IMAGE
)
import pygame


class Player(BaseSpaceship):
    """
    Класс корабля игрока.
    """
    def __init__(self, screen, object_positions, img):
        super().__init__(screen, object_positions, img)
        self.object_positions.set_position('player', RES_X/2, RES_Y/2)
        self.destroyed = False
        self.shot_type = 'base'
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

    def get_shot_type(self):
        return self.shot_type

    def check_active_bonuses(self):
        to_delete = []
        for bonus_type in self.active_bonuses:
            self.active_bonuses[bonus_type] += 1
            if self.active_bonuses[bonus_type] >= 360:
                to_delete.append(bonus_type)
                if bonus_type == 'shot':
                    self.set_shot_type()

        for item in to_delete:
            self.active_bonuses.pop(item, False)
