from cmd.helpers.ObjectHelper import rot_center
from BaseSpaceship import BaseSpaceship
from cmd.config.config import RES_X, RES_Y
import pygame


class Player(BaseSpaceship):
    """
    Класс корабля игрока.
    """
    def __init__(self, screen, object_positions, img):
        super().__init__(screen, object_positions, img)
        self.object_positions.set_position('player', RES_X/2, RES_Y/2)

        self.debugimg = pygame.image.load("png/debug.png")

    def draw(self):
        player_image, new_rect = rot_center(self.img,
                                            self.orientation,
                                            RES_X/2-20,
                                            RES_Y/2-24)
        self.screen.blit(player_image, (RES_X/2-int(new_rect.width/2), RES_Y/2-int(new_rect.height/2)))
