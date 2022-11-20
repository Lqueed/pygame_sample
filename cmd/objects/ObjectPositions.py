import random
import uuid
import math

from cmd.helpers.ObjectHelper import rot_center, random_fn
from cmd.objects.BaseSpaceship import BaseSpaceship
from cmd.objects.BaseMob import BaseMob
from cmd.objects.BigMob import BigMob
from cmd.objects.SatteliteMob import SatteliteMob
from cmd.objects.BaseBomb import BaseBomb
from cmd.objects.BaseBonus import BaseBonus
from cmd.objects.BaseMinimap import Minimap
from cmd.objects.StarDestroyerBoss import StarDestroyer
from cmd.objects.CorvetteBoss import Corvette
from cmd.config.config import (
    BASE_MOB_IMG,
    SPAWN_RATE,
    EXPLOSION_IMAGE,
    RES_X,
    RES_Y,
    ARROWS_TO_MOB,
    BOMB_EXPLOSION_RADIUS,
    BONUS_IMG,
    BONUS_SPAWN_CHANCE,
    BIG_MOB_IMG,
    SATTELITE_MOB_IMAGE,
    MINIMAP,
    STAR_DESTROYER_IMG,
    CORVETTE_IMG,
    DOUBLE_BONUS_IMG
)


class ObjectPositions:
    """
    Общий класс для хранения объектов мобов, выстрелов и тд
    Все методы по движению и взаимодействию объектов вызываем через этот класс
    """
    def __init__(self, screen, stats, sounds):
        self.sounds = sounds
        self.stats = stats
        self.player = ()  # тут храним координаты
        self.player_obj = None
        self.mobs = {}
        self.shots = {}
        self.bombs = {}
        self.bonuses = {}
        self.boss = None
        self.enemy_shots = {}
        self.player_x_size = 20  # mock
        self.player_y_size = 20  # mock
        self.mob_x_size_small = 24
        self.mob_y_size_small = 24
        self.screen = screen
        self.minimap = Minimap(screen=self.screen)
        self.kill_count = 0
        self.boss_level = False
        self.boss_ready = False
        
    def add_boss(self, spawn_coords=(0, 0)):
        boss_id = str(uuid.uuid4())
        if random.randint(0, 1):
            self.boss = StarDestroyer(
                img=STAR_DESTROYER_IMG,
                screen=self.screen,
                boss_id=boss_id,
                object_positions=self,
            )
        else:
            self.boss = Corvette(
                img=CORVETTE_IMG,
                screen=self.screen,
                boss_id=boss_id,
                object_positions=self,
            )
        return self.boss

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

    def add_mob(self, img, screen, object_positions, spawn_coords=None):
        mob_id = str(uuid.uuid4())
        self.mobs[mob_id] = BaseMob(
            img=img,
            screen=screen,
            mob_id=mob_id,
            object_positions=object_positions,
            spawn_coords=spawn_coords,
        )
        return mob_id

    def add_mob_group(self, count: int = random.randint(2, 5)):
        mob_id = self.add_mob(img=BASE_MOB_IMG, screen=self.screen, object_positions=self)
        pos_x_main = self.mobs[mob_id].abs_pos_x
        pos_y_main = self.mobs[mob_id].abs_pos_y

        spawned_big = False
        for i in range(count - 1):
            angle = random.randint(0, 360) - i * (360/count)
            new_coords = (pos_x_main + 200 * math.cos(angle), pos_y_main + 200 * math.sin(angle))
            if not spawned_big and random.randint(0, 1):
                self.add_big_mob(img=BIG_MOB_IMG, screen=self.screen, object_positions=self, spawn_coords=new_coords)
                spawned_big = True
            else:
                self.add_mob(img=BASE_MOB_IMG, screen=self.screen, object_positions=self, spawn_coords=new_coords)

    def add_sattelite_mob(self, img, screen, object_positions, coords):
        self.mobs[str(uuid.uuid4())] = SatteliteMob(
            img=img,
            screen=screen,
            mob_id=str(uuid.uuid4()),
            object_positions=object_positions,
            spawn_coords=coords,
            orientation=self.player_obj.orientation - 90
        )
        self.mobs[str(uuid.uuid4())] = SatteliteMob(
            img=img,
            screen=screen,
            mob_id=str(uuid.uuid4()),
            object_positions=object_positions,
            spawn_coords=coords,
            orientation=self.player_obj.orientation + 90
        )

    def add_big_mob(self, img, screen, object_positions, spawn_coords=None):
        mob_id = str(uuid.uuid4())
        self.mobs[mob_id] = BigMob(
            img=img,
            screen=screen,
            mob_id=mob_id,
            object_positions=object_positions,
            spawn_coords=spawn_coords,
        )

    def clear_mobs(self):
        self.mobs = {}

    def clear_shots(self):
        self.shots = {}
        self.enemy_shots = {}

    def clear_all(self):
        self.clear_shots()
        self.clear_mobs()
        self.bombs = {}
        self.bonuses = {}

    def add_player(self, player):
        self.player_obj = player

    def add_shot(self, angle, shot_type='base'):
        pos_x = self.player[0]
        pos_y = self.player[1]
        shot_id = str(uuid.uuid4())
        self.player_obj.shoot(
            pos_x=pos_x,
            pos_y=pos_y,
            shot_id=shot_id,
            angle=angle,
            shot_type=shot_type
        )

    def add_bomb(self, img):
        pos_x = self.player[0]
        pos_y = self.player[1]
        bomb_id = str(uuid.uuid4())
        self.bombs[bomb_id] = BaseBomb(
            id=bomb_id,
            object_positions=self,
            img=img,
            angle=0,
            pos_x=pos_x,
            pos_y=pos_y,
            screen=self.screen
        )
        self.bombs[bomb_id].spawn()

    def add_bonus(self, pos_x=None, pos_y=None):
        bonus_id = str(uuid.uuid4())
        bonus_type = random.randint(0, 1)
        if bonus_type:
            bonus_type = 'power'
            bonus_img = BONUS_IMG
        else:
            bonus_type = 'double'
            bonus_img = DOUBLE_BONUS_IMG

        self.bonuses[bonus_id] = BaseBonus(
            id=bonus_id,
            img=bonus_img,
            screen=self.screen,
            object_positions=self,
            type=bonus_type,
        )
        if pos_x and pos_y:
            self.bonuses[bonus_id].spawn_coords(pos_x, pos_y)
        else:
            self.bonuses[bonus_id].spawn_random()

    def move_shots(self, left, right, up, down):
        to_delete = []
        for shot_id, shot in self.shots.items():
            shot.move()
            if shot.age >= 180:
                to_delete.append(shot_id)
        for shot_id in to_delete:
            self.shots.pop(shot_id, None)

        for shot_id, shot in self.enemy_shots.items():
            shot.move(left, right, up, down)
            if shot.age >= 180:
                to_delete.append(shot_id)
        for shot_id in to_delete:
            self.enemy_shots.pop(shot_id, None)

    def move_objects(self, left, right, up, down):
        for mob_id, mob_obj in self.mobs.items():
            mob_obj.move(left, right, up, down)
            mob_obj.move_mob()
        for bomb_id, bomb_obj in self.bombs.items():
            bomb_obj.move(left, right, up, down)
        for bonus_id, bonus_obj in self.bonuses.items():
            bonus_obj.move(left, right, up, down)
        if self.boss:
            self.boss.move(left, right, up, down)

        self.spawn_boss_level()
        if not self.boss_level:
            self.spawn_more_mobs_random()

    def draw_player(self):
        self.player_obj.draw()

    def draw_mobs(self):
        for _, mob in self.mobs.items():
            mob.draw()
            if ARROWS_TO_MOB and not mob.is_destroyed and mob.type not in ['rocket']:
                mob.draw_line_to_player()

    def draw_bosses(self):
        if self.boss:
            self.boss.draw()

    def draw_bombs(self):
        for _, bomb in self.bombs.items():
            bomb.draw_bomb()

    def draw_bonuses(self):
        for _, bonus in self.bonuses.items():
            bonus.draw_bonus()

    def draw_shots(self):
        for _, shot in self.shots.items():
            shot.draw_shot()
        for _, shot in self.enemy_shots.items():
            shot.draw_shot()

    def draw_all(self):
        self.draw_bosses()
        self.draw_shots()
        self.draw_bombs()
        self.draw_bonuses()
        self.draw_mobs()
        self.draw_player()
        self.stats.draw()
        if MINIMAP:
            self.minimap.draw(self.mobs)
        self.draw_text()

        self.check_active_bonuses()

    def find_collisions(self):
        """
        Ищет пересечения хитбоксов выстрелов, мобов и игрока
        """
        mobs = self.detect_collisions_pl()
        mobs += self.detect_collisions_shots()
        collided_mobs, collided_bombs = self.detect_collisions_bombs()
        mobs += collided_mobs
        for m_id in mobs:
            if m_id in self.mobs:
                self.mobs[m_id].destroy_ship(img=EXPLOSION_IMAGE)
                if self.mobs[m_id].type == 'big':
                    self.add_sattelite_mob(img=SATTELITE_MOB_IMAGE,
                                           screen=self.screen,
                                           object_positions=self,
                                           coords=(self.mobs[m_id].pos_x, self.mobs[m_id].pos_y))

        for b_id in collided_bombs:
            if b_id in self.bombs:
                self.bombs[b_id].destroy_bomb(img=EXPLOSION_IMAGE)

        bonuses = self.detect_collisions_bonuses()
        for b_id in bonuses:
            self.bonuses.pop(b_id, None)

        if self.boss:
            if self.boss.detect_collisions_pl(player_obj=self.player,
                                         player_x_size=self.player_x_size,
                                         player_y_size=self.player_y_size):
                self.player_obj.destroy_player()
            self.boss.detect_collisions_shots(object_positions=self)

        self.destroy_timer()
        self.move_mobs_group()

    def destroy_timer(self):
        """
        Таймер до уничтожения объекта - пока показываем спрайт взрыва
        """
        to_delete_mobs = []
        spawn_bonus = random_fn(BONUS_SPAWN_CHANCE)

        for m_id in self.mobs:
            if self.mobs[m_id].destroy_count >= 60:
                to_delete_mobs.append(m_id)
                self.stats.increase_score(10)
                if self.mobs[m_id].type != 'sattelite':
                    self.kill_count += 1
        for m_id in to_delete_mobs:
            if spawn_bonus:
                self.add_bonus(pos_x=self.mobs[m_id].pos_x,
                               pos_y=self.mobs[m_id].pos_y)
                spawn_bonus = False
            self.mobs.pop(m_id, None)

        if self.boss:
            to_delete = self.boss.destroy_timer()
            if spawn_bonus:
                for turret_id in to_delete:
                    self.add_bonus(pos_x=self.boss.turrets[turret_id].pos_x,
                                   pos_y=self.boss.turrets[turret_id].pos_y)
                    spawn_bonus = False
                    break
            self.boss.delete_turrets(to_delete)

        to_delete_bombs = []
        for b_id in self.bombs:
            if self.bombs[b_id].destroy_count >= 60:
                to_delete_bombs.append(b_id)
        for b_id in to_delete_bombs:
            self.bombs.pop(b_id, None)

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

        shot_to_del = []
        for shot_id, coords in self.enemy_shots.items():
            if (coords.pos_x <= self.player[0] + self.player_x_size and \
                coords.pos_x >= self.player[0] - self.player_x_size) \
                    and (coords.pos_y <= self.player[1] + self.player_y_size and \
                         coords.pos_y >= self.player[1] - self.player_y_size):
                shot_to_del.append(shot_id)
                self.player_obj.destroy_player()
        for shot_id in shot_to_del:
            self.enemy_shots.pop(shot_id, None)

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
                         abs(shot_data.pos_y) >= coords.pos_y - self.mob_y_size_small) \
                    and not coords.is_destroyed:
                    collided.append(mob_id)
                    if not shot_data.power:
                        shot_to_del.append(shot_id)
                    self.stats.increase_score(10)
        for shot_id in shot_to_del:
            self.shots.pop(shot_id, None)
        return collided

    def detect_collisions_bombs(self):
        """
        Ищем столкновения бомб с мобами и игроком
        """
        collided_mob = []
        collided_bomb = []

        for bomb_id, coords in self.bombs.items():
            if (coords.pos_x <= self.player[0] + self.player_x_size and \
                coords.pos_x >= self.player[0] - self.player_x_size) \
                    and (coords.pos_y <= self.player[1] + self.player_y_size and \
                         coords.pos_y >= self.player[1] - self.player_y_size) \
                    and coords.aggressive:
                collided_bomb.append(bomb_id)
                self.player_obj.destroy_player()

        for mob_id, coords in self.mobs.items():
            for bomb_id, bmb_c in self.bombs.items():
                if (coords.pos_x <= bmb_c.pos_x + BOMB_EXPLOSION_RADIUS and \
                    coords.pos_x >= bmb_c.pos_x - BOMB_EXPLOSION_RADIUS) \
                    and (coords.pos_y <= bmb_c.pos_y + BOMB_EXPLOSION_RADIUS and \
                         coords.pos_y >= bmb_c.pos_y - BOMB_EXPLOSION_RADIUS) \
                    and not coords.is_destroyed\
                    and bmb_c.aggressive:
                    collided_mob.append(mob_id)
                    collided_bomb.append(bomb_id)

        return collided_mob, collided_bomb

    def detect_collisions_bonuses(self):
        collided = []
        for bonus_id, coords in self.bonuses.items():
            if (coords.pos_x <= self.player[0] + self.player_x_size and \
                coords.pos_x >= self.player[0] - self.player_x_size) \
                    and (coords.pos_y <= self.player[1] + self.player_y_size and \
                         coords.pos_y >= self.player[1] - self.player_y_size):
                collided.append(bonus_id)
                self.player_obj.set_bonus(coords.type)
        return collided

    def spawn_more_mobs_random(self):
        if len(self.mobs) == 0 and not self.boss:
            if random.randint(0, SPAWN_RATE) == 0:
                self.add_mob_group()

    def spawn_bonus_random(self):
        if random.randint(0, SPAWN_RATE) == 0:
            for _ in range(1):
                self.add_bonus()

    def del_too_far_objects(self):
        to_delete = []
        for mob_id, mob in self.mobs.items():
            if mob.pos_x - self.player[0] > RES_X * 3 or mob.pos_y - self.player[1] > RES_Y * 3:
                to_delete.append(mob_id)
        for mob_id in to_delete:
            self.mobs.pop(mob_id, None)

        for s_id, shot in self.shots.items():
            if shot.pos_x - self.player[0] > RES_X * 3 or shot.pos_y - self.player[1] > RES_Y * 3:
                to_delete.append(s_id)
        for s_id in to_delete:
            self.shots.pop(s_id, None)

    def get_player_shot_type(self):
        return self.player_obj.get_shot_type()

    def check_active_bonuses(self):
        self.player_obj.check_active_bonuses()

    def get_mobs_angle(self, mob1_id, mob2_id):
        angle = math.atan2(self.mobs[mob1_id].pos_y - self.mobs[mob2_id].pos_y,
                           self.mobs[mob1_id].pos_x - self.mobs[mob2_id].pos_x)
        return angle

    def move_mobs_group(self):
        GROUP_DISTANCE = 100
        mob_coords_arr = {}
        for mob1_id, mob1 in self.mobs.items():
            for mob2_id, mob2 in self.mobs.items():
                if mob1_id != mob2_id and\
                        abs(mob1.abs_pos_x - mob2.abs_pos_x) <= GROUP_DISTANCE and \
                        abs(mob1.abs_pos_y - mob2.abs_pos_y) <= GROUP_DISTANCE and \
                        mob1.type != 'sattelite':
                    if (mob2_id not in mob_coords_arr or mob_coords_arr[mob2_id] != mob1_id) \
                            and mob1_id not in mob_coords_arr:
                        mob_coords_arr[mob1_id] = mob2_id
        for mob_id in mob_coords_arr:
            angle = self.get_mobs_angle(mob_id, mob_coords_arr[mob_id])
            self.mobs[mob_id].group_move(angle)

    def spawn_boss_level(self):
        if self.boss_level and not self.boss_ready:
            player_angle_rotate = BaseSpaceship.smooth_rotate_to_angle(0, orientation=self.player_obj.orientation)
            self.player_obj.set_orientation(player_angle_rotate)

            dist_pl_boss = int(math.sqrt(
                (self.boss.pos_x - self.player[0]) ** 2 + (self.boss.pos_y - self.player[1]) ** 2
            ))
            if player_angle_rotate == self.player_obj.orientation and abs(dist_pl_boss) <= self.boss.height * 1.5:
                self.boss_ready = True

        if self.boss_level:
            if self.boss.is_defeated:
                self.kill_count = 0

                player_angle_rotate = BaseSpaceship.smooth_rotate_to_angle(0, orientation=self.player_obj.orientation)
                self.player_obj.set_orientation(player_angle_rotate)
                dist_pl_boss = self.boss.pos_y - self.player[1]
                if dist_pl_boss >= RES_Y:
                    self.kill_count = 0
                    self.boss_level = False
                    self.boss_ready = False
                    self.boss = None

        if not self.boss_level:
            if self.kill_count >= 10: # and not self.mobs:
                self.kill_count = 0
                self.boss_level = True
                boss = self.add_boss()
                boss.spawn(spawn_coords=(self.player[0] - boss.width/2, self.player[1]-3000))

    def draw_text(self):
        if self.boss_level and not self.boss_ready:
            self.stats.draw_boss_prepare()

        if self.boss and self.boss.is_defeated:
            self.stats.draw_mobs_prepare()
