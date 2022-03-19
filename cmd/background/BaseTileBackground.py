import pygame


class BaseTileBackground:
    def __init__(self, screen, img: str = None):
        self.tile_img = pygame.image.load(img)
        self.screen = screen
        self.pos_x = 0
        self.pos_y = 0
        self.resolution = (1024, 1024)  # пока хардкод

    def set_position(self, pos_x, pos_y):
        if pos_x >= self.resolution[0] or pos_x <= -self.resolution[0]:
            self.pos_x = 0
        else:
            self.pos_x = pos_x
        if pos_y >= self.resolution[1] or pos_y <= -self.resolution[1]:
            self.pos_y = 0
        else:
            self.pos_y = pos_y

    def get_position(self):
        return self.pos_x, self.pos_y

    def set_background_img(self):
        self.screen.blit(self.tile_img, (self.pos_x, self.pos_y))
        if abs(self.pos_x) >= self.resolution[0]:
            self.pos_x = 0
        if abs(self.pos_y) >= self.resolution[1]:
            self.pos_y = 0
        dir_x = BaseTileBackground.get_direction(self.pos_x)
        dir_y = BaseTileBackground.get_direction(self.pos_y)
        if self.pos_x != 0 or self.pos_x != 0:
            self.screen.blit(self.tile_img, (self.pos_x + dir_x * self.resolution[0],
                                             self.pos_y + dir_y * self.resolution[1]))
            if self.pos_y != 0:
                self.screen.blit(self.tile_img, (self.pos_x,
                                                 self.pos_y + dir_y * self.resolution[1]))
            if self.pos_x != 0:
                self.screen.blit(self.tile_img, (self.pos_x + dir_x * self.resolution[0],
                                                 self.pos_y))

    @staticmethod
    def get_direction(pos):
        if pos > 0:
            return -1
        elif pos < 0:
            return 1
        elif pos == 0:
            return 0
