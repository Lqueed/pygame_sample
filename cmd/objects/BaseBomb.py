from cmd.helpers.ObjectHelper import rot_center
import pygame
from cmd.config.config import EXPLOSION_IMAGE


class BaseBomb:
    """
    Базовый класс для бомб - хранит состояние, координаты, угол, id и таймер
    """
    def __init__(self, id, object_positions, img, angle, pos_x, pos_y, screen):
        self.id = id
        self.object_positions = object_positions
        self.img = img
        self.angle = angle
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.abs_pos_x = 0
        self.abs_pos_y = 0
        self.screen = screen
        self.age = 0
        self.aggressive = False
        self.is_destroyed = False
        self.destroy_count = 0

    def move(self,
             left=None,
             right=None,
             up=None,
             down=None):
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

    def set_bomb_img(self, img: str = None):
        self.img = pygame.image.load(img)

    def draw_bomb(self):
        if self.age >= 10:
            self.aggressive = True
        if self.age >= 120:
            self.is_destroyed = True
            self.destroy_bomb(img=EXPLOSION_IMAGE)

        if not self.is_destroyed:
            if self.age % 10 == 0:
                self.angle += 18
                if self.angle >= 360:
                    self.angle = 0

            img, new_rect = rot_center(self.img, self.angle, self.abs_pos_x, self.abs_pos_y)
            self.screen.blit(img,
                             (self.abs_pos_x - int(new_rect.width / 2),
                              self.abs_pos_y - int(new_rect.height / 2)))
            self.age += 1
        else:
            self.destroy_count += 1
            self.screen.blit(self.img,
                             (self.abs_pos_x - 10,
                              self.abs_pos_y - 10))

    def spawn(self):
        self.abs_pos_x = self.pos_x
        self.abs_pos_y = self.pos_y

    def destroy_bomb(self, img):
        self.is_destroyed = True
        self.set_bomb_img(img=img)