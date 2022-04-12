from BaseMob import BaseMob


class BigMob(BaseMob):
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
        super().__init__(screen=screen,
                         img=img,
                         object_positions=object_positions,
                         mob_id=mob_id,
                         spawn_coords=spawn_coords,
                         aggressive=aggressive)

        self.type = 'big'
