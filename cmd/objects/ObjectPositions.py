from cmd.helpers.ObjectHelper import rot_center
from cmd.objects.BaseShot import BaseShot
import uuid


class ObjectPositions:
    def __init__(self, screen):
        self.player = ()
        self.mobs = {}
        self.shots = {}
        self.player_x_size = 20
        self.player_y_size = 20
        self.screen = screen

    def set_position(self, object_type, pos_x, pos_y, mob_id=0):
        if object_type == 'player':
            self.player = (pos_x, pos_y)
        if object_type == 'mob':
            self.mobs[mob_id] = (pos_x, pos_y)

    def del_object(self, object_type, obj_id):
        if object_type == 'mob':
            self.mobs.pop(obj_id, None)

    def detect_collisions(self):
        collided = []
        for mob_id, coords in self.mobs.items():
            if (coords[0] <= self.player[0] + self.player_x_size and \
                coords[0] >= self.player[0] - self.player_x_size)\
                and (coords[1] <= self.player[1] + self.player_y_size and \
                     coords[1] >= self.player[1] - self.player_y_size):
                collided.append(mob_id)
        return collided

    def add_shot(self, img, angle):
        pos_x = self.player[0] + self.player_x_size
        pos_y = self.player[1] + self.player_y_size
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

    def detect_collisions_shots(self):
        collided = []
        shot_to_del = []
        for shot_id, shot_data in self.shots.items():
            for mob_id, coords in self.mobs.items():
                if (abs(shot_data.pos_x) <= coords[0] + self.player_x_size and \
                    abs(shot_data.pos_x) >= coords[0] - self.player_x_size)\
                    and (abs(shot_data.pos_y) <= coords[1] + self.player_y_size and \
                         abs(shot_data.pos_y) >= coords[1] - self.player_y_size):
                    collided.append(mob_id)
                    shot_to_del.append(shot_id)
        for shot_id in shot_to_del:
            self.shots.pop(shot_id)
        return collided
