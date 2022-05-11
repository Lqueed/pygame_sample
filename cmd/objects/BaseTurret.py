import uuid
import pygame
import math

from cmd.helpers.ObjectHelper import rot_center
from cmd.objects.BaseMob import BaseMob
from cmd.objects.EnemyShot import EnemyShot
from cmd.config.config import (
    TURRET_SHOOT_DELAY,
    TURRET_SHOT_SPEED,
)


class BaseTurret(BaseMob):
    """
    Базовый класс для туррелей - хранит состояние, координаты, угол, id и таймер
    """
    def __init__(self, id, object_positions, img, screen, aggressive_distance):
        super().__init__(screen=screen,
                         img=img,
                         object_positions=object_positions,
                         aggressive_distance=aggressive_distance)
        self.id = id
        self.object_positions = object_positions
        self.img = pygame.image.load(img)
        self.angle = 0
        self.screen = screen
        self.orientation = 0
        self.age = 0
        self.shoot_delay = 0

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
            return
        else:
            self.rotate()

        if self.is_player_near():
            self.shoot()

    def rotate(self):
        angle = - int(math.degrees(self.angle_to_player()) + 90)
        self.set_orientation(angle)

    def draw(self, img: str = None):
        pos_x = self.abs_pos_x
        pos_y = self.abs_pos_y

        ship_image, new_rect = rot_center(self.img, self.orientation, self.pos_x-self.width/2, self.pos_y-self.height/2)
        self.screen.blit(ship_image, (pos_x - int(new_rect.width / 2), pos_y - int(new_rect.height / 2)))

    def shoot(self):
        if self.shoot_delay == 0:
            shot_id = str(uuid.uuid4())
            self.object_positions.enemy_shots[shot_id] = EnemyShot(
                id=shot_id,
                object_positions=self,
                angle=self.orientation,
                pos_x=self.pos_x,
                pos_y=self.pos_y,
                screen=self.screen,
                shot_speed=TURRET_SHOT_SPEED
            )
            self.shoot_delay = TURRET_SHOOT_DELAY
            self.object_positions.enemy_shots[shot_id].draw_shot()
            self.object_positions.sounds.sound_shot()
        else:
            self.shoot_delay -= 1
