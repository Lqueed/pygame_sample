import pygame
from cmd.objects.Player import Player
from cmd.objects.BaseMob import BaseMob
from cmd.objects.ObjectPositions import ObjectPositions
from cmd.background.TileBackground import TileBackground
from cmd.helpers.KeyHelper import detect_player_move, detect_player_rotate

display_size = (1024, 1024)
pygame.init()
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("pygame test")

speed = 5

object_positions = ObjectPositions()

player = Player(img="png/x-wing-small.png",
                screen=screen,
                object_positions=object_positions)

bg = TileBackground(img="png/tile_bg.jpg",
                    screen=screen)

mobs = {}
mobs[0] = BaseMob(img="png/x-wing-small-inverted.png",
                  screen=screen,
                  mob_id=0,
                  object_positions=object_positions)
mobs[1] = BaseMob(img="png/x-wing-small-inverted.png",
                  screen=screen,
                  mob_id=1,
                  object_positions=object_positions)
mobs[2] = BaseMob(img="png/x-wing-small-inverted.png",
                  screen=screen,
                  mob_id=2,
                  object_positions=object_positions)
for mob_id, mob_cl in mobs.items():
    mob_cl.spawn_random()

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
    for mob_id, mob_obj in mobs.items():
        mob_obj.move(left, right, up, down)
        mob_obj.move_random()

    col_mob_ids = object_positions.detect_collisions()

    for m_id in col_mob_ids:
        mobs[m_id].destroy_ship(img="png/explosion.png")
        if mobs[m_id].destroy_count >= 60:
            mobs.pop(m_id, None)

    bg.draw()
    player.draw()
    for mob_id, mob_obj in mobs.items():
        mob_obj.draw()

    pygame.display.update()

pygame.quit()