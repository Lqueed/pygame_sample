import pygame
from cmd.objects.Player import Player
from cmd.objects.BaseMob import BaseMob
from cmd.background.TileBackground import TileBackground
from cmd.helpers.KeyHelper import detect_player_move, detect_player_rotate

display_size = (1024, 1024)
pygame.init()
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("pygame test")

speed = 5

player = Player(img="png/x-wing-small.png", screen=screen)
bg = TileBackground(img="png/tile_bg.jpg", screen=screen)

mob = BaseMob(img="png/x-wing-small-inverted.png", screen=screen)
mob.spawn_random()

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # передвижение верх-низ-лево-право
    # delta_x, delta_y, changed, left, right, up, down = detect_player_move(keys, speed)
    # player.get_set_orientation(delta_x, delta_y, changed)

    # передвижение поворот + вперед-назад
    move_speed, left, right = detect_player_rotate(keys, speed)
    left, right, up, down = player.get_set_rotation(move_speed, left, right)

    bg.move(left, right, up, down)
    mob.move(left, right, up, down)
    mob.move_random()

    bg.draw()
    player.draw()
    mob.draw()

    pygame.display.update()

pygame.quit()