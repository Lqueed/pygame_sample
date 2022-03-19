import pygame
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((1024, 1024))
pygame.display.set_caption("pygame test")

speed = 10


class Player:
    def __init__(self, screen, img: str = None):
        self.screen = screen
        self.img = pygame.image.load(img)
        self.orientation = 0

    def get_player_img(self):
        return self.img

    def set_orientation(self, delta_x: int = 0, delta_y: int = 0, changed: bool = False):
        if not changed:
            return
        if delta_x == 0 and delta_y >= 0:
            self.orientation = 0
        elif delta_x == 0 and delta_y < 0:
            self.orientation = 180
        elif delta_x < 0 and delta_y == 0:
            self.orientation = 270
        elif delta_x > 0 and delta_y == 0:
            self.orientation = 90
        elif delta_x > 0 and delta_y < 0:
            self.orientation = 135
        elif delta_x < 0 and delta_y < 0:
            self.orientation = 225
        elif delta_x > 0 and delta_y > 0:
            self.orientation = 45
        elif delta_x < 0 and delta_y > 0:
            self.orientation = 315

    def draw(self):
        player_image, new_rect = rot_center(self.img, self.orientation, 512-20, 512-24)
        self.screen.blit(player_image, (512-20, 512-24))


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect


class Background:
    def __init__(self, screen, img: str = None):
        self.tile_img = pygame.image.load(img)
        self.screen = screen
        self.pos_x = 0
        self.pos_y = 0
        self.resolution = (1024, 1024)  # пока хардкод

    def set_position(self, pos_x, pos_y):
        if pos_x >= self.resolution[0] or pos_x <= -self.resolution[0]:
            self.pos_x = 0
        else:
            self.pos_x = pos_x
        if pos_y >= self.resolution[1] or pos_y <= -self.resolution[1]:
            self.pos_y = 0
        else:
            self.pos_y = pos_y

    def get_position(self):
        return self.pos_x, self.pos_y

    def get_background_img(self):
        self.screen.blit(self.tile_img, (self.pos_x, self.pos_y))
        if self.pos_x >= self.resolution[0]:
            self.pos_x = 0
        if self.pos_y >= self.resolution[1]:
            self.pos_y = 0
        dir_x = Background.get_dir(self.pos_x)
        dir_y = Background.get_dir(self.pos_y)
        if self.pos_x != 0 or self.pos_x != 0:
            self.screen.blit(self.tile_img, (self.pos_x + dir_x * self.resolution[0],
                                             self.pos_y + dir_y * self.resolution[1]))
            if self.pos_y != 0:
                self.screen.blit(self.tile_img, (self.pos_x,
                                                 self.pos_y + dir_y * self.resolution[1]))
            if self.pos_x != 0:
                self.screen.blit(self.tile_img, (self.pos_x + dir_x * self.resolution[0],
                                                 self.pos_y))
        # print(self.pos_x, self.pos_y)
        # print(self.pos_x + dir_x * self.resolution[0],
        #       self.pos_y + dir_y * self.resolution[1])
        # print('')

    @staticmethod
    def get_dir(pos):
        if pos > 0:
            return -1
        elif pos < 0:
            return 1
        elif pos == 0:
            return 0


player = Player(img="png/x-wing-small.png", screen=screen)
bg = Background(img="png/tile_bg.jpg", screen=screen)

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    delta_x = 0
    delta_y = 0
    changed = False
    if keys[pygame.K_LEFT]:
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            bg.pos_x += int(speed * 1.41)
        else:
            bg.pos_x += speed
        delta_x = 1
        changed = True
    if keys[pygame.K_RIGHT]:
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            bg.pos_x -= int(speed * 1.41)
        else:
            bg.pos_x -= speed
        delta_x = -1
        changed = True
    if keys[pygame.K_UP]:
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            bg.pos_y += int(speed * 1.41)
        else:
            bg.pos_y += speed
        delta_y = 1
        changed = True
    if keys[pygame.K_DOWN]:
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            bg.pos_y -= int(speed * 1.41)
        else:
            bg.pos_y -= speed
        delta_y = -1
        changed = True

    player.set_orientation(delta_x, delta_y, changed)
    bg.get_background_img()
    player.draw()

    pygame.display.update()

pygame.quit()