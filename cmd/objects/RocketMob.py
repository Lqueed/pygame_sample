from BaseMob import BaseMob
from cmd.config.config import (
    ROCKET_SHOT_SPEED,
    ROCKET_IMG
)


class RocketMob(BaseMob):
    """
    Базовый класс для всех мобов - хранит состояние, координаты и id
    Наследуется в т.ч. от фона - для расчета движения мобов вместе с фоном
    """
    def __init__(self,
                 screen,
                 object_positions,
                 orientation,
                 mob_id=0,
                 spawn_coords=(),
                 aggressive=False,):
        super().__init__(screen=screen,
                         img=ROCKET_IMG,
                         object_positions=object_positions,
                         mob_id=mob_id,
                         spawn_coords=spawn_coords,
                         aggressive=aggressive)

        self.speed = ROCKET_SHOT_SPEED
        self.type = 'rocket'
        self.orientation = orientation

    def is_player_near(self):
        return True
