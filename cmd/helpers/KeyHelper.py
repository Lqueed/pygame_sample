import pygame
from cmd.config.config import (
    PAUSE_KEY,
    SHOOT_KEY_MAIN,
)

class KeyHelper:
    def __init__(self):
        self.key_press_delay = 0
        self.pause_key = PAUSE_KEY
        self.shoot_key = SHOOT_KEY_MAIN

    # Класс помощник для работы с нажатиями на кнопки
    @staticmethod
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

    @staticmethod
    def detect_player_rotate(keys, speed: int = 10):
        """
        повороты и вперед-назад
        """
        left = None
        right = None

        speed_input = 5    # хардкод - постоянный полет со скоростью 10

        # if keys[pygame.K_UP]:
        #     speed_input = speed
        # if keys[pygame.K_DOWN]:
        #     speed_input = -speed
        if keys[pygame.K_LEFT]:
            left = True
        if keys[pygame.K_RIGHT]:
            right = True

        return speed_input, left, right

    def detect_shoot(self, keys):
        """
        пиу пиу
        """
        shoot = False
        if keys[self.shoot_key]:
            shoot = True
        return shoot

    @staticmethod
    def detect_free_flight(keys):
        """
        полет с выключенными движками
        """
        free_flight = False
        if keys[pygame.K_LCTRL]:
            free_flight = True
        return free_flight

    def detect_pause(self, keys):
        """
        пауза игры
        """
        if self.key_press_delay == 0 and keys[self.pause_key]:
            self.key_press_delay = 10
            return True
        # на всякий случай
        elif self.key_press_delay < 0:
            self.key_press_delay = 0
            return False
        else:
            self.key_press_delay -= 1
            return False

    @staticmethod
    def detect_esc(keys):
        return keys[pygame.K_ESCAPE]
