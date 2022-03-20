from cmd.helpers.ObjectHelper import rot_center
from BaseSpaceship import BaseSpaceship
from cmd.background.BaseTileBackground import BaseTileBackground
from cmd.objects.ObjectPositions import ObjectPositions
import random


class BaseMob(BaseSpaceship, BaseTileBackground):
    def __init__(self,
                 screen,
                 img,
                 object_positions: ObjectPositions,
                 mob_id=0,
                 spawn_coords=(),
                 aggressive=True):
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

    def spawn(self, spawn_coords: tuple = (0, 0)):
        pass

    def spawn_random(self):
        self.pos_x = random.randint(0, 512)
        self.pos_y = random.randint(0, 512)
        self.abs_pos_x = self.pos_x
        self.abs_pos_y = self.pos_y

    def draw(self):
        pos_x = self.abs_pos_x
        pos_y = self.abs_pos_y
        ship_image, new_rect = rot_center(self.img, self.orientation, self.pos_x-20, self.pos_y-24)
        self.screen.blit(ship_image, (pos_x, pos_y))

    def move_random(self):
        if not self.is_destroyed:
            if self.sleep_frames_count:
                self.sleep_frames_count -= 1

            elif self.random_moving:
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
        else:
            self.destroy_count += 1

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
        self.future_move_orientation = self.get_orientation(-delta_x, -delta_y, changed)

    def destroy_ship(self, img):
        self.set_ship_img(img)
        self.is_destroyed = True
        self.object_positions.del_object('mob', self.mob_id)
