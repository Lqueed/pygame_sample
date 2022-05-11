import uuid

from cmd.objects.BaseTurret import BaseTurret
from cmd.objects.RocketMob import RocketMob
from cmd.config.config import (
    ROCKET_TURRET_SHOOT_DELAY
)


class RocketTurret(BaseTurret):
    def __init__(self, id, object_positions, img, screen, aggressive_distance):
        super().__init__(id=id,
                         screen=screen,
                         img=img,
                         object_positions=object_positions,
                         aggressive_distance=aggressive_distance)
        self.angle = 0
        self.age = 0
        self.shoot_delay = 0

        self.width = int(self.img.get_rect().size[0])
        self.height = int(self.img.get_rect().size[1])

    def shoot(self):
        if self.shoot_delay == 0:
            shot_id = str(uuid.uuid4())
            self.object_positions.mobs[shot_id] = RocketMob(
                object_positions=self.object_positions,
                screen=self.screen,
                orientation=self.orientation
            )
            rocket = self.object_positions.mobs[shot_id]
            rocket.spawn(spawn_coords=(self.abs_pos_x, self.abs_pos_y))
            rocket.draw()
            self.shoot_delay = ROCKET_TURRET_SHOOT_DELAY
            # self.object_positions.sounds.sound_shot()
        else:
            self.shoot_delay -= 1
