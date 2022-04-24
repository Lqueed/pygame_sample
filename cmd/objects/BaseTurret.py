from cmd.helpers.ObjectHelper import rot_center
import pygame
import math
from cmd.config.config import EXPLOSION_IMAGE
from cmd.objects.BaseMob import BaseMob


class BaseTurret(BaseMob):
    """
    Базовый класс для туррелей - хранит состояние, координаты, угол, id и таймер
    """
    def __init__(self, id, object_positions, img, screen):
        super().__init__(screen=screen, img=img, object_positions=object_positions)
        self.id = id
        self.object_positions = object_positions
        self.img = pygame.image.load(img)
        self.angle = 0
        self.pos_x = 0
        self.pos_y = 0
        self.abs_pos_x = 0
        self.abs_pos_y = 0
        self.screen = screen
        self.orientation = 0
        self.age = 0
        self.aggressive = False
        self.is_destroyed = False
        self.destroy_count = 0

        self.width = int(self.img.get_rect().size[0])
        self.height = int(self.img.get_rect().size[1])

    def angle_to_player(self):
        player_coords = self.object_positions.player
        angle = math.atan2(player_coords[1] - self.pos_y, player_coords[0] - self.pos_x)
        return angle

    def move(self,
             left=None,
             right=None,
             up=None,
             down=None):
        super().move(left=left,
                     right=right,
                     up=up,
                     down=down)
        if self.is_destroyed:
            # таймер до полного удаления
            self.destroy_count += 1
        else:
            self.rotate()

    def rotate(self):
        angle = - int(math.degrees(self.angle_to_player()) + 90)
        self.set_orientation(angle)

    def draw(self, img: str = None):
        pos_x = self.abs_pos_x
        pos_y = self.abs_pos_y

        ship_image, new_rect = rot_center(self.img, self.orientation, self.pos_x-self.width/2, self.pos_y-self.height/2)
        self.screen.blit(ship_image, (pos_x - int(new_rect.width / 2), pos_y - int(new_rect.height / 2)))
