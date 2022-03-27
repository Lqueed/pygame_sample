from cmd.helpers.ObjectHelper import rot_center
from BaseSpaceship import BaseSpaceship
from cmd.background.BaseTileBackground import BaseTileBackground
import random
import math
from cmd.config.config import (
    RES_X,
    RES_Y,
    AGGRESIVE_DISTANSE,
    MOB_SPEED
)


class BaseMob(BaseSpaceship, BaseTileBackground):
    """
    Базовый класс для всех мобов - хранит состояние, координаты и id
    Наследуется в т.ч. от фона - для расчета движения мобов вместе с фоном
    """
    def __init__(self,
                 screen,
                 img,
                 object_positions,
                 mob_id=0,
                 spawn_coords=(),
                 aggressive=False):
        super().__init__(screen=screen, img=img, object_positions=object_positions)
        self.aggressive = aggressive
        self.pos_x = 0
        self.pos_y = 0
        self.abs_pos_x = 0
        self.abs_pos_y = 0
        self.mob_id = mob_id

        self.is_destroyed = False
        self.destroy_count = 0

        if not spawn_coords:
            self.spawn_random()
        else:
            self.spawn(spawn_coords)

        self.random_moving_speed_direction = None
        self.random_moving = False
        self.drift_frames_limit = 0
        self.drift_frames_count = 0
        self.sleep_frames_count = 0

        self.future_move_orientation = None

    def set_position(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def spawn(self, spawn_coords: tuple = (0, 0)):
        """
        Потом тут будет логика спавна корабля по триггеру
        """
        pass

    def spawn_random(self):
        """
        спавним в рандомно пределах экрана (пока что) - потом будем спавнить за пределами экрана
        """
        self.pos_x = random.randint(0, RES_X)
        self.pos_y = random.randint(0, RES_Y)

        # self.pos_x = random.choice([-RES_X - random.randint(-RES_X, 0), RES_X + random.randint(0, RES_X)])
        # self.pos_y = random.choice([-RES_Y - random.randint(-RES_Y, 0), RES_Y + random.randint(0, RES_Y)])

        self.abs_pos_x = self.pos_x
        self.abs_pos_y = self.pos_y

    def draw(self):
        pos_x = self.abs_pos_x
        pos_y = self.abs_pos_y

        ship_image, new_rect = rot_center(self.img, self.orientation, self.pos_x-20, self.pos_y-24)
        self.screen.blit(ship_image, (pos_x - int(new_rect.width / 2), pos_y - int(new_rect.height / 2)))

    def is_player_near(self):
        player_coords = self.object_positions.player
        dist = int(math.sqrt((self.pos_x - player_coords[0]) ** 2 + (self.pos_y - player_coords[1]) ** 2))
        return dist <= AGGRESIVE_DISTANSE

    def move_mob(self):
        """
        Движение корабля в рандомных направлениях
        """
        if self.is_destroyed:
            # таймер до полного удаления
            self.destroy_count += 1
        else:
            if self.is_player_near():
                self.move_to_player()

            elif self.sleep_frames_count:
                self.sleep_frames_count -= 1

            else:
                self.move_random()

    def move_random(self):
        if self.random_moving:
            # если в движении - двигаем
            if self.future_move_orientation is not None:
                self.set_orientation(self.future_move_orientation)
            self.drift_frames_count += 1
            self.move(left=self.random_moving_speed_direction[0],
                      right=self.random_moving_speed_direction[1],
                      up=self.random_moving_speed_direction[2],
                      down=self.random_moving_speed_direction[3])
            if self.drift_frames_count >= self.drift_frames_limit:
                self.random_moving = False
                self.drift_frames_count = 0

        else:
            # если не в движении - считаем куда двигать
            self.drift_frames_limit = random.randint(30, 120)
            self.sleep_frames_count = random.randint(30, 150)
            delta_x = random.randint(-1, 1)
            delta_y = random.randint(-1, 1)
            changed = bool(delta_x or delta_y)
            left = 0
            right = 0
            up = 0
            down = 0

            if delta_x and delta_x > 0:
                left = random.randint(0, 3)
            if delta_x and delta_x < 0:
                right = random.randint(0, 3)

            if delta_y and delta_y > 0:
                up = random.randint(0, 3)
            elif delta_y and delta_y < 0:
                down = random.randint(0, 3)

            self.set_future_orientation(delta_x, delta_y, changed)

            self.random_moving_speed_direction = (left, right, up, down)
            self.random_moving = True

    def move_to_player(self):
        pass
        player_coords = self.object_positions.player
        angle = - int(math.degrees(math.atan2(player_coords[1] - self.pos_y,
                                              player_coords[0] - self.pos_x)) + 90)
        self.set_orientation(angle)
        left, right, up, down = self.calculate_move(MOB_SPEED)
        self.move(left, right, up, down)

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

        self.object_positions.set_position('mob', self.abs_pos_x, self.abs_pos_y, self.mob_id)

    def set_future_orientation(self, delta_x, delta_y, changed):
        """
        Направить нос корабля в ту сторону, в которую он потом полетит
        """
        self.future_move_orientation = self.get_orientation(-delta_x, -delta_y, changed)

    def destroy_ship(self, img):
        """
        Запускает таймер до уничтожения корабля и меняет спрайт корабля на спрайт взрыва
        """
        self.set_ship_img(img)
        self.is_destroyed = True
