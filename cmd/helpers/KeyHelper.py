import pygame
from cmd.config.config import (
    PAUSE_KEY,
    SHOOT_KEY_MAIN,
    FREE_FLIGHT_KEY,
    BOMB_KEY
)

class KeyHelper:
    def __init__(self, main_menu):
        self.main_menu = main_menu
        self.key_press_delay = 0
        self.pause_key = PAUSE_KEY
        self.shoot_key = SHOOT_KEY_MAIN
        self.free_flight = FREE_FLIGHT_KEY
        self.bomb_key = BOMB_KEY

    @staticmethod
    def detect_menu_btn_press(btn_coords):
        mouse = pygame.mouse.get_pos()
        if not btn_coords:
            return False
        if (btn_coords[0] <= mouse[0] <= btn_coords[0] + btn_coords[2]) and \
                btn_coords[1] <= mouse[1] <= btn_coords[1] + btn_coords[3]:
            return True
        return False

    def detect_clear_lb_press(self):
        if pygame.mouse.get_pressed()[0] and self.main_menu.shown:
            btn_coords = self.main_menu.get_clear_lb_coords()
            if KeyHelper.detect_menu_btn_press(btn_coords=btn_coords):
                self.main_menu.clear_leaderboard()

    def detect_quit_press(self):
        if pygame.mouse.get_pressed()[0] and self.main_menu.shown:
            btn_coords = self.main_menu.get_quit_coords()
            return KeyHelper.detect_menu_btn_press(btn_coords=btn_coords)

    # нажатие кнопки Старт в меню - по координатам
    def detect_start_press(self):
        if pygame.mouse.get_pressed()[0] and self.main_menu.shown:
            btn_coords = self.main_menu.get_start_coords()
            if KeyHelper.detect_menu_btn_press(btn_coords=btn_coords):
                self.main_menu.show_hide_menu()
                return True

    def detect_leaderboard_press(self):
        if pygame.mouse.get_pressed()[0] and self.main_menu.shown:
            btn_coords = self.main_menu.get_leaderboard_coords()
            if KeyHelper.detect_menu_btn_press(btn_coords=btn_coords):
                self.main_menu.leaderboard_shown = 1
                return True

    def detect_back_press(self):
        if pygame.mouse.get_pressed()[0] and self.main_menu.shown and self.main_menu.leaderboard_shown:
            btn_coords = self.main_menu.get_back_coords()
            if KeyHelper.detect_menu_btn_press(btn_coords=btn_coords):
                self.main_menu.leaderboard_shown = 0
                return True

    def detect_clear_press(self):
        if pygame.mouse.get_pressed()[0] and self.main_menu.shown and self.main_menu.leaderboard_shown:
            btn_coords = self.main_menu.get_clear_lb_coords()
            if KeyHelper.detect_menu_btn_press(btn_coords=btn_coords):
                self.main_menu.clear_leaderboard()
                return True

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

    def detect_bomb_drop(self, keys):
        """
        пиу пиу
        """
        shoot = False
        if keys[self.bomb_key]:
            shoot = True
        return shoot

    def detect_free_flight(self, keys):
        """
        полет с выключенными движками
        """
        free_flight = False
        if keys[self.free_flight]:
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
