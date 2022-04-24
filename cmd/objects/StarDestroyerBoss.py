from BaseBoss import BaseBoss
from BaseTurret import BaseTurret
from cmd.config.config import (TURRET_PNG)
import uuid


class StarDestroyer(BaseBoss):
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
            (262, 1493),
            (262, 1554),
            (704, 1493),
            (704, 1554),
            (243, 1250),
            (243, 1250),
            (246, 1084),
            (726, 1084),
            (275, 557),
            (691, 557),
        ]
