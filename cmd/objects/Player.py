from cmd.helpers.ObjectHelper import rot_center
from BaseSpaceship import BaseSpaceship


class Player(BaseSpaceship):
    def __init__(self, screen, object_positions, img):
        super().__init__(screen, object_positions, img)
        self.object_positions.set_position('player', 512, 512)

    def draw(self):
        player_image, new_rect = rot_center(self.img, self.orientation, 512-20, 512-24)
        self.screen.blit(player_image, (512-20, 512-24))