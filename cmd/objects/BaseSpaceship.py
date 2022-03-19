from cmd.helpers.ObjectHelper import rot_center
import pygame


class BaseSpaceship:
    def __init__(self, screen, img: str = None):
        self.screen = screen
        self.img = pygame.image.load(img)
        self.orientation = 0

    def set_ship_img(self, img: str = None):
        self.img = pygame.image.load(img)

    def set_orientation(self, delta_x: int = 0, delta_y: int = 0, changed: bool = False):
        if not changed:
            return
        if delta_x == 0 and delta_y >= 0:
            self.orientation = 0
        elif delta_x > 0 and delta_y > 0:
            self.orientation = 45
        elif delta_x > 0 and delta_y == 0:
            self.orientation = 90
        elif delta_x > 0 and delta_y < 0:
            self.orientation = 135
        elif delta_x == 0 and delta_y < 0:
            self.orientation = 180
        elif delta_x < 0 and delta_y == 0:
            self.orientation = 270
        elif delta_x < 0 and delta_y < 0:
            self.orientation = 225
        elif delta_x < 0 and delta_y > 0:
            self.orientation = 315

    def draw(self):
        player_image, new_rect = rot_center(self.img, self.orientation, 512-20, 512-24)
        self.screen.blit(player_image, (512-20, 512-24))
