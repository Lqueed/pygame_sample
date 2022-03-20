import pygame


def detect_player_move(keys, bg, speed: int = 10):
    delta_x = 0
    delta_y = 0
    changed = False
    left = None
    right = None
    up = None
    down = None

    if keys[pygame.K_LEFT]:
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            left = int(speed * 1.41)
        else:
            left = speed
        delta_x = 1
        changed = True
    if keys[pygame.K_RIGHT]:
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            right = int(speed * 1.41)
        else:
            right = speed
        delta_x = -1
        changed = True
    if keys[pygame.K_UP]:
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            up = int(speed * 1.41)
        else:
            up = speed
        delta_y = 1
        changed = True
    if keys[pygame.K_DOWN]:
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            down = int(speed * 1.41)
        else:
            down = speed
        delta_y = -1
        changed = True

    return delta_x, delta_y, changed, left, right, up, down
