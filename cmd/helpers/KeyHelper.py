import pygame


# Класс помощник для работы с нажатиями на кнопки
def detect_player_move(keys, speed: int = 10):
    """
    дискретно - вверх вниз влево вправо
    """
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


def detect_player_rotate(keys, speed: int = 10):
    """
    повороты и вперед-назад
    """
    left = None
    right = None

    speed_input = 0
    if keys[pygame.K_UP]:
        speed_input = speed
    if keys[pygame.K_LEFT]:
        left = True
    if keys[pygame.K_RIGHT]:
        right = True
    if keys[pygame.K_DOWN]:
        speed_input = -speed

    return speed_input, left, right


def detect_shoot(keys):
    """
    пиу пиу
    """
    shoot = False
    if keys[pygame.K_SPACE]:
        shoot = True
    return shoot
