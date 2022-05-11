from cmd.config.config import (
    TURRET_PNG,
    EXPLOSION_IMAGE,
    TURRET_AGGRESIVE_DISTANSE,
    ROCKET_TURRET_PNG
)
import pygame
import uuid
from BaseTurret import BaseTurret
from RocketTurret import RocketTurret


class BaseBoss:
    def __init__(self,
                 screen,
                 img,
                 object_positions,
                 boss_id=0):
        self.img = pygame.image.load(img)
        self.screen = screen
        self.object_positions = object_positions
        self.pos_x = 0
        self.pos_y = 0
        self.abs_pos_x = 0
        self.abs_pos_y = 0
        self.boss_id = boss_id
        self.turrets = {}
        self.turret_coords = []
        self.rocket_turret_coords = []
        self.is_defeated = False

        self.width = self.img.get_rect().size[0]
        self.height = self.img.get_rect().size[1]

    def set_position(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def spawn(self, spawn_coords: tuple = (0, 0)):
        self.pos_x = spawn_coords[0]
        self.pos_y = spawn_coords[1]
        self.abs_pos_x = self.pos_x
        self.abs_pos_y = self.pos_y

        self.spawn_turrets()

    def draw(self):
        pos_x = self.abs_pos_x
        pos_y = self.abs_pos_y
        self.screen.blit(self.img, (pos_x, pos_y))

        for _, turret in self.turrets.items():
            turret.draw()

        if not self.turrets:
            self.is_defeated = True

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

        for _, turret in self.turrets.items():
            turret.move(left, right, up, down)

    def spawn_turrets(self):
        for tur_coords in self.turret_coords:
            tur_id = uuid.uuid4()
            turret_obj = self.turrets[tur_id] = BaseTurret(
                id=tur_id,
                object_positions=self.object_positions,
                img=TURRET_PNG,
                screen=self.screen,
                aggressive_distance=TURRET_AGGRESIVE_DISTANSE,
            )
            turret_obj.spawn(
                spawn_coords=(tur_coords[0] + self.abs_pos_x + turret_obj.width/2,
                              tur_coords[1] + self.abs_pos_y + turret_obj.height/2)
            )

        for rock_tur in self.rocket_turret_coords:
            tur_id = uuid.uuid4()
            turret_obj = self.turrets[tur_id] = RocketTurret(
                id=tur_id,
                object_positions=self.object_positions,
                img=ROCKET_TURRET_PNG,
                screen=self.screen,
                aggressive_distance=TURRET_AGGRESIVE_DISTANSE,
            )
            turret_obj.spawn(
                spawn_coords=(rock_tur[0] + self.abs_pos_x + turret_obj.width/2,
                              rock_tur[1] + self.abs_pos_y + turret_obj.height/2)
            )

    def destroy_turrets(self, list_turrets: list):
        for tur in list_turrets:
            self.turrets[tur].destroy_ship(img=EXPLOSION_IMAGE)

    def detect_collisions_pl(self, player_obj, player_x_size, player_y_size):
        """
        Ищем столкновения мобов с игроком
        """
        collided = []
        for tur_id, coords in self.turrets.items():
            if (coords.pos_x <= player_obj[0] + player_x_size and \
                    coords.pos_x >= player_obj[0] - player_x_size) \
                    and (coords.pos_y <= player_obj[1] + player_y_size and \
                         coords.pos_y >= player_obj[1] - player_y_size) \
                    and not coords.is_destroyed:
                collided.append(tur_id)
        self.destroy_turrets(collided)
        return collided

    def detect_collisions_shots(self, object_positions):
        """
        Ищем столкновения мобов с выстрелами
        """
        collided = []
        shot_to_del = []
        for shot_id, shot_data in object_positions.shots.items():
            for mob_id, coords in self.turrets.items():
                if (abs(shot_data.pos_x) <= coords.pos_x + coords.width and \
                    abs(shot_data.pos_x) >= coords.pos_x - coords.height)\
                    and (abs(shot_data.pos_y) <= coords.pos_y + coords.width and \
                         abs(shot_data.pos_y) >= coords.pos_y - coords.height) \
                    and not coords.is_destroyed:
                    collided.append(mob_id)
                    if not shot_data.power:
                        shot_to_del.append(shot_id)
                    object_positions.stats.increase_score(10)
        for shot_id in shot_to_del:
            object_positions.shots.pop(shot_id, None)

        self.destroy_turrets(collided)
        return collided

    def destroy_timer(self):
        to_delete = []
        for t_id in self.turrets:
            if self.turrets[t_id].destroy_count >= 60:
                to_delete.append(t_id)
                self.object_positions.stats.increase_score(10)
        return to_delete

    def delete_turrets(self, to_delete: list):
        for t_id in to_delete:
            self.turrets.pop(t_id, None)
