import pygame
import sys
import os
import json
from cmd.config.config import *
from cmd.helpers.TextHelper import draw_text
from pygame.locals import *
from pathlib import Path

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

BLACK = (0,0,0)

# класс для главного меню
class BaseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.quit_coords = ()
        self.start_coords = ()
        self.leaderboard_coords = ()
        self.back_coords = ()
        self.clear_lb_coords = ()
        self.shown = True
        self.leaderboard_shown = False
        self.save_score_coords = ()
        self.back_menu_coords = ()

    def draw_menu(self):
        self.screen.fill(BLACK)
        # задаем текст каждого пунка и отрисовываем через помощник
        font_size = int(RES_Y/15)
        menu_font = pygame.font.Font(resource_path(os.path.join('cmd/fonts', 'Rexagus.ttf')), font_size)

        if self.leaderboard_shown:
            draw_text(self.screen, menu_font, "Leaderboard", (200, 200, 200), (RES_X/2, RES_Y/6))
            self.draw_leaderboard()
            return

        draw_text(self.screen, menu_font, "Star Wars, but shitty", (200, 200, 200), (RES_X/2, RES_Y/3))

        font_size = int(RES_Y/20)
        menu_font = pygame.font.Font(resource_path(os.path.join('cmd/fonts', 'Rexagus.ttf')), font_size)
        self.start_coords = draw_text(self.screen, menu_font, "Start", (200, 200, 200), (RES_X/2, RES_Y/2), True)
        self.leaderboard_coords = draw_text(self.screen,
                                            menu_font,
                                            "Leaderboard",
                                            (200, 200, 200),
                                            (RES_X/2, RES_Y/2 + int(font_size * 1.5)),
                                            True)
        draw_text(self.screen, menu_font, "Options", (200, 200, 200), (RES_X/2, RES_Y/2 + int(font_size * 3)), True)
        self.quit_coords = draw_text(self.screen,
            menu_font, "Quit", (200, 200, 200), (RES_X/2, RES_Y/2 + int(font_size * 4.5)), True)

    def show_hide_menu(self):
        self.shown = not self.shown

    # получить координаты кнопки на экране
    def get_quit_coords(self):
        if self.quit_coords:
            return self.quit_coords
        return None

    def get_back_menu_coords(self):
        if self.back_menu_coords:
            return self.back_menu_coords
        return None

    def get_save_score_coords(self):
        if self.save_score_coords:
            return self.save_score_coords
        return None

    def get_start_coords(self):
        if self.start_coords:
            return self.start_coords
        return None

    def get_back_coords(self):
        if self.back_coords:
            return self.back_coords
        return None

    def get_leaderboard_coords(self):
        if self.leaderboard_coords:
            return self.leaderboard_coords
        return None

    def get_clear_lb_coords(self):
        if self.clear_lb_coords:
            return self.clear_lb_coords
        return None

    def draw_leaderboard(self):
        font_size = int(RES_Y/15)
        menu_font = pygame.font.Font(resource_path(os.path.join('cmd/fonts', 'Rexagus.ttf')), font_size)
        try:
            with open('leaderboard.json', 'r+') as fp:
                leaderboard_json = json.load(fp)
        except FileNotFoundError:
            self.clear_leaderboard()
            leaderboard_json = {}

        score_x_coord = RES_Y/3
        count_scored = 0
        for player_name, score in {k: v for k, v in sorted(leaderboard_json.items(), key=lambda item: item[1])}.items():
            if count_scored >= 5:
                break
            draw_text(self.screen, menu_font, f"{player_name}: {int(score)}", (200, 200, 200), (RES_X/2, score_x_coord))
            score_x_coord += RES_Y/10
            count_scored += 1

        self.back_coords = draw_text(self.screen,
            menu_font, "Back", (200, 200, 200), (RES_X/1.1, RES_Y/1.7 + int(font_size * 4.5)), True)

        self.clear_lb_coords = draw_text(self.screen,
            menu_font, "Clear", (200, 200, 200), (RES_X/2, RES_Y/1.7 + int(font_size * 4.5)), True)

    def clear_leaderboard(self):
        with open('leaderboard.json', 'w+') as fp:
            leaderboard_json = {}
            json.dump(leaderboard_json, fp)

    def save_score(self, player_name: str, score: int):
        if not Path("leaderboard.json").is_file():
            self.clear_leaderboard()
        with open('leaderboard.json', 'r+') as fp:
            leaderboard_json = json.load(fp)
            leaderboard_json[player_name] = score
            fp.seek(0)
            json.dump(leaderboard_json, fp)
            fp.truncate()

        self.shown = 1
        self.leaderboard_shown = 1
