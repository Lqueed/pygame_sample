import pygame
from PIL import Image
from cmd.objects.Player import Player
from cmd.background.TileBackground import TileBackground
from cmd.helpers.KeyHelper import detect_player_move

pygame.init()
screen = pygame.display.set_mode((1024, 1024))
pygame.display.set_caption("pygame test")

speed = 5

player = Player(img="png/x-wing-small.png", screen=screen)
bg = TileBackground(img="png/tile_bg.jpg", screen=screen)

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    delta_x, delta_y, changed = detect_player_move(keys, bg, speed)
    player.set_orientation(delta_x, delta_y, changed)

    bg.set_background_img()
    player.draw()

    pygame.display.update()

pygame.quit()