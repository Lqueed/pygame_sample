from BaseBoss import BaseBoss


class Corvette(BaseBoss):
    def __init__(self,
                 screen,
                 img,
                 object_positions,
                 boss_id=0):
        super().__init__(screen=screen,
                         img=img,
                         object_positions=object_positions,
                         boss_id=boss_id)

        self.turret_coords = [
            (455, 6),
            (455, 980),
            (1074, 611),
            (1074, 382),
            (524, 493),
            (162, 411),
            (162, 580),
        ]

        self.rocket_turret_coords = [
            (1304, 519),
        ]
