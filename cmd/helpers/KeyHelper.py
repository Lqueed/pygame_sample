import pygame


def detect_player_move(keys, bg, speed: int = 10):
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

    return delta_x, delta_y, changed
