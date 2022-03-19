import pygame
from PIL import Image

bg = pygame.image.load("png/background.jpg")
player_gif = "png/duck.gif"


def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        ret.append(pygame_image)
    return ret


class Player:
    def __init__(self, gif=None):
        self.gif = gif
        self.player_frame = 0
        self.frames = split_animated_gif(self.gif)
        self.player_frames = len(self.frames)
        self.need_change_frame = 0
        self.orientation = 'right'

    def get_frame(self):
        frame = self.frames[self.player_frame]
        self.need_change_frame += 1
        if self.need_change_frame >= 2:
            self.player_frame += 1
            if self.player_frame >= self.player_frames:
                self.player_frame = 0
            self.need_change_frame = 0
        if self.orientation == 'right':
            return frame
        else:
            return pygame.transform.flip(frame, True, False)


pygame.init()
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("pygame test")

x = 50
y = 50
speed = 5

player = Player(gif=player_gif)

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.orientation = 'left'
        x -= speed
    if keys[pygame.K_RIGHT]:
        player.orientation = 'right'
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    win.blit(bg, (0, 0))
    win.blit(player.get_frame(), (x, y))
    pygame.display.update()

pygame.quit()