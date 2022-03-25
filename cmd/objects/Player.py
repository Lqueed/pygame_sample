from cmd.helpers.ObjectHelper import rot_center
from BaseSpaceship import BaseSpaceship
import pygame


class Player(BaseSpaceship):
    """
    Класс корабля игрока.
    """
    def __init__(self, screen, object_positions, img):
        super().__init__(screen, object_positions, img)
        self.object_positions.set_position('player', 512, 512)

        self.debugimg = pygame.image.load("png/debug.png")

    def draw(self):
        ###
        debugimg, new_rects = rot_center(self.debugimg, self.orientation, 512-20, 512-24)  # DEBUG
        self.screen.blit(debugimg, (512-20, 512-24))  # DEBUG
        ###

        player_image, new_rect = rot_center(self.img, self.orientation, 512-20, 512-24)
        self.screen.blit(player_image, (512-20, 512-24))