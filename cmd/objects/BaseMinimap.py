import pygame
import cmd.config.config as config


class Minimap:
    def __init__(self,
                 screen):
        self.screen = screen
        self.x_size = 70
        self.y_size = self.x_size / (config.RES_X / config.RES_Y)
        self.x_offset = 30 + self.x_size
        self.y_offset = 30 + self.y_size
        self.ratio = config.RES_X / self.x_size
        self.luc_x = config.RES_X - (self.x_size * 2 + self.x_offset)
        self.luc_y = self.y_offset - self.y_size

    def draw_minimap(self):
        # black rect
        pygame.draw.rect(self.screen,
                         (0, 0, 0),
                         pygame.Rect(self.luc_x,
                                     self.luc_y,
                                     self.x_size * 3,
                                     self.y_size * 3))
        # rect border
        pygame.draw.rect(self.screen,
                         (50, 50, 50),
                         pygame.Rect(self.luc_x,
                                     self.luc_y,
                                     self.x_size * 3,
                                     self.y_size * 3),
                         1)

    def draw_player(self):
        pygame.draw.rect(self.screen,
                         (0, 255, 0),
                         pygame.Rect(config.RES_X - (self.x_size + self.x_offset) + self.x_size/2 - 1,
                                     self.y_offset + self.y_size / 2 - 1,
                                     2,
                                     2))

    def draw_mob(self, mob):
        pos_x = mob.abs_pos_x / self.ratio
        pos_y = mob.abs_pos_y / self.ratio
        coord_x = config.RES_X - (self.x_size + self.x_offset) + pos_x
        coord_y = self.y_offset + pos_y
        color = (255, 0, 0)
        if mob.is_destroyed:
            color = (125, 125, 125)
        if coord_x > self.luc_x + 1 and \
                coord_x < self.luc_x + self.x_size * 3 - 2 and \
                coord_y > self.luc_y + 1 and \
                coord_y < self.luc_y + self.y_size * 3 - 2:
            pygame.draw.rect(self.screen,
                             color,
                             pygame.Rect(coord_x,
                                         coord_y,
                                         2,
                                         2))

    def draw_mobs(self, mobs):
        for _, mob in mobs.items():
            self.draw_mob(mob)

    def draw(self, mobs):
        self.draw_minimap()
        self.draw_mobs(mobs)
        self.draw_player()
