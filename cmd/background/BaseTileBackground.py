from cmd.config.config import RES_X, RES_Y
import pygame


class BaseTileBackground:
    """
    Базовый класс фона - хранит положение фона относительно игрока и мету фоновой картинки
    Содержит методы для движения фона, заполнения экрана тайлами и отрисовки фона
    """
    def __init__(self, screen, img: str = None):
        self.tile_img = pygame.image.load(img)
        self.screen = screen
        self.pos_x = 0
        self.pos_y = 0
        self.abs_pos_x = 0
        self.abs_pos_y = 0
        self.resolution = (1024, 1024)  # пока хардкод

    def set_position(self, pos_x, pos_y):
        """
        Задаем позицию для лву фона
        """
        self.abs_pos_x = pos_x
        if pos_x >= self.resolution[0] or pos_x <= -self.resolution[0]:
            self.pos_x = 0
        else:
            self.pos_x = pos_x

        self.abs_pos_y = pos_y
        if pos_y >= self.resolution[1] or pos_y <= -self.resolution[1]:
            self.pos_y = 0
        else:
            self.pos_y = pos_y

    def get_position(self):
        return self.pos_x, self.pos_y

    def draw(self):
        """
        Отрисовываем тайлы (центральный + в тех местах где экран не заполнен фоном)
        """
        self.screen.blit(self.tile_img, (self.pos_x, self.pos_y))
        if abs(self.pos_x) >= self.resolution[0]:
            self.pos_x = 0
        if abs(self.pos_y) >= self.resolution[1]:
            self.pos_y = 0
        dir_x = BaseTileBackground.get_direction(self.pos_x)
        dir_y = BaseTileBackground.get_direction(self.pos_y)
        if self.pos_x != 0 or self.pos_y != 0:
            # TODO: разобраться и сделать нормально
            self.screen.blit(self.tile_img, (self.pos_x + dir_x * self.resolution[0],
                                             self.pos_y + dir_y * self.resolution[1]))
            self.screen.blit(self.tile_img, (self.pos_x + dir_x*2 * self.resolution[0],
                                             self.pos_y + dir_y * self.resolution[1]))

            #
            self.screen.blit(self.tile_img, (self.pos_x - self.resolution[0],
                                             self.pos_y))
            self.screen.blit(self.tile_img, (self.pos_x + self.resolution[0],
                                             self.pos_y))
            #

            if self.pos_y != 0:
                self.screen.blit(self.tile_img, (self.pos_x,
                                                 self.pos_y + dir_y * self.resolution[1]))
                self.screen.blit(self.tile_img, (self.pos_x + self.resolution[0],
                                                 self.pos_y + dir_y * self.resolution[1]))
            if self.pos_x != 0:
                self.screen.blit(self.tile_img, (self.pos_x + dir_x * self.resolution[0],
                                                 self.pos_y))
                self.screen.blit(self.tile_img, (self.pos_x + self.resolution[0],
                                                 self.pos_y))

    @staticmethod
    def get_direction(pos):
        """
        метод-помощник, нужен только для фона
        """
        if pos > 0:
            return -1
        elif pos < 0:
            return 1
        elif pos == 0:
            return 0

    def move(self,
             left=None,
             right=None,
             up=None,
             down=None):
        """
        Двигаем фон в зависимости от псевдодвижения игрока
        """
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
