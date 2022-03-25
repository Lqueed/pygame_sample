import random
import uuid

from cmd.helpers.ObjectHelper import rot_center
from cmd.objects.BaseShot import BaseShot
from cmd.objects.BaseMob import BaseMob
from cmd.config.config import (
    BASE_MOB_IMG,
    SPAWN_RATE,
    EXPLOSION_IMAGE,
    RES_X,
    RES_Y
)


class ObjectPositions:
    """
    Общий класс для хранения объектов мобов, выстрелов и тд
    Все методы по движению и взаимодействию объектов вызываем через этот класс
    """
    def __init__(self, screen):
        self.player = ()  # тут храним координаты
        self.player_obj = None
        self.mobs = {}
        self.shots = {}
        self.player_x_size = 20  # mock
        self.player_y_size = 20  # mock
        self.mob_x_size_small = 24
        self.mob_y_size_small = 24
        self.screen = screen

    def set_position(self, object_type, pos_x, pos_y, mob_id=0):
        if object_type == 'player':
            self.player = (pos_x, pos_y)
        if object_type == 'mob':
            self.mobs[mob_id].set_position(pos_x, pos_y)

    def del_object(self, object_type, obj_id):
        """
        Уничтожить объект
        """
        if object_type == 'mob':
            self.mobs.pop(obj_id, None)

    def add_mob(self, img, screen, object_positions):
        mob_id = str(uuid.uuid4())
        self.mobs[mob_id] = BaseMob(
            img=img,
            screen=screen,
            mob_id=mob_id,
            object_positions=object_positions
        )
        self.mobs[mob_id].spawn_random()

    def add_player(self, player):
        self.player_obj = player

    def add_shot(self, img, angle):
        pos_x = self.player[0]
        pos_y = self.player[1]
        rotated_shot, _ = rot_center(img, angle, pos_x, pos_y)
        shot_id = str(uuid.uuid4())
        self.shots[shot_id] = BaseShot(
            id=shot_id,
            object_positions=self,
            img=rotated_shot,
            angle=angle,
            pos_x=pos_x,
            pos_y=pos_y,
            screen=self.screen
        )
        self.shots[shot_id].draw_shot()

    def move_shots(self):
        to_delete = []
        for shot_id, shot in self.shots.items():
            shot.move()
            if shot.age >= 180:
                to_delete.append(shot_id)
        for shot_id in to_delete:
            self.shots.pop(shot_id)

    def move_mobs(self, left, right, up, down):
        for mob_id, mob_obj in self.mobs.items():
            mob_obj.move(left, right, up, down)
            mob_obj.move_random()

    def draw_player(self):
        self.player_obj.draw()

    def draw_mobs(self):
        for _, mob in self.mobs.items():
            mob.draw()

    def draw_all(self):
        self.draw_mobs()
        self.draw_player()

    def find_collisions(self):
        """
        Ищет пересечения хитбоксов выстрелов, мобов и игрока
        """
        mobs = self.detect_collisions_pl()
        mobs += self.detect_collisions_shots()
        for m_id in mobs:
            if m_id in self.mobs:
                self.mobs[m_id].destroy_ship(img=EXPLOSION_IMAGE)
        self.destroy_timer()

    def destroy_timer(self):
        """
        Таймер до уничтожения объекта - пока показываем спрайт взрыва
        """
        to_delete = []
        for m_id in self.mobs:
            if self.mobs[m_id].destroy_count >= 60:
                to_delete.append(m_id)
        for m_id in to_delete:
            self.mobs.pop(m_id, None)

    def detect_collisions_pl(self):
        """
        Ищем столкновения мобов с игроком
        """
        collided = []
        for mob_id, coords in self.mobs.items():
            if (coords.pos_x <= self.player[0] + self.player_x_size and \
                coords.pos_x >= self.player[0] - self.player_x_size) \
                and (coords.pos_y <= self.player[1] + self.player_y_size and \
                     coords.pos_y >= self.player[1] - self.player_y_size) \
                and not coords.is_destroyed:
                collided.append(mob_id)
                self.player_obj.destroy_player()
        return collided

    def detect_collisions_shots(self):
        """
        Ищем столкновения мобов с выстрелами
        """
        collided = []
        shot_to_del = []
        for shot_id, shot_data in self.shots.items():
            for mob_id, coords in self.mobs.items():
                if (abs(shot_data.pos_x) <= coords.pos_x + self.mob_x_size_small and \
                    abs(shot_data.pos_x) >= coords.pos_x - self.mob_x_size_small)\
                    and (abs(shot_data.pos_y) <= coords.pos_y + self.mob_y_size_small and \
                         abs(shot_data.pos_y) >= coords.pos_y - self.mob_y_size_small):
                    collided.append(mob_id)
                    shot_to_del.append(shot_id)
        for shot_id in shot_to_del:
            self.shots.pop(shot_id)
        return collided

    def spawn_more_mobs_random(self):
        if len(self.mobs) == 0:
            if random.randint(0, SPAWN_RATE) == 0:
                for _ in range(3):
                    self.add_mob(img=BASE_MOB_IMG,
                                 screen=self.screen,
                                 object_positions=self)

    def del_too_far_mobs(self):
        to_delete = []
        for mob_id, mob in self.mobs.items():
            if mob.pos_x - self.player[0] > RES_X * 3 or mob.pos_y - self.player[1] > RES_Y * 3:
                to_delete.append(mob_id)
        for mob_id in to_delete:
            self.mobs.pop(mob_id)
