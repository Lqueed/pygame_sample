from cmd.config.config import (
    RES_X,
    RES_Y,
    GAME_SPEED_FPS,
    PLAYER_LIVES
)
import pygame
import time
from cmd.helpers.TextHelper import *


class BaseStats:
    def __init__(self,
                 screen,
                 main_menu,
                 key_helper):
        self.screen = screen
        self.score = 0
        self.time_spent = 0
        self.frame_count = 0
        self.lives = PLAYER_LIVES
        self.name_input = None
        self.main_menu = main_menu
        self.key_helper = key_helper

    def add_input_box(self):
        from cmd.helpers.TextHelper import InputBox
        self.name_input = InputBox(
            RES_X/2 - 150,
            100,
            300,
            40,
            self.screen
        )

    def increase_score(self, delta: int):
        self.score += delta

    def increase_time(self):
        self.frame_count += 1
        if self.frame_count >= GAME_SPEED_FPS:
            self.frame_count = 0
            self.time_spent += 1

    def draw(self):
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 20))
        score_surface = myfont.render(f'Score: {int(self.score)}', False, (255, 255, 255))
        self.screen.blit(score_surface, (int(RES_X / 40), int(RES_Y / 40)))

        if self.time_spent >= 3600:
            time_str = f'Time: {time.strftime("%H:%M:%S", time.gmtime(int(self.time_spent)))}'
        else:
            time_str = f'Time: {time.strftime("%M:%S", time.gmtime(int(self.time_spent)))}'
        time_surface = myfont.render(time_str, False, (255, 255, 255))
        self.screen.blit(time_surface, (int(RES_X / 40), int(RES_Y / 40) + int(RES_Y / 40) + int(RES_Y / 40)/2))
        self.draw_lives()

    def draw_endgame(self):
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 5))
        text_surface = myfont.render('YOU FUCKED UP', False, (255, 255, 255))
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 15))
        self.screen.blit(text_surface, (RES_X / 2 - int(RES_X / 3.2), RES_Y / 2 - int(RES_Y / 20)))
        draw_text(self.screen,
                  myfont,
                  f'Score: {self.score}', (200, 200, 200), (RES_X / 2, RES_Y / 1.7 + int(RES_Y/15)), True)

        if not self.name_input:
            self.add_input_box()
        for event in pygame.event.get():
            self.name_input.handle_event(event)
        self.name_input.update()
        self.name_input.draw()

        font_size = int(RES_Y/15)
        menu_font = pygame.font.Font(resource_path(os.path.join('cmd/fonts', 'Rexagus.ttf')), font_size)

        # TODO: make active
        self.main_menu.save_score_coords = draw_text(self.screen,
            menu_font, "Save score", (200, 200, 200), (RES_X/2, RES_Y/1.7 + int(font_size * 4.5)), True)
        self.main_menu.back_menu_coords = draw_text(self.screen,
            menu_font, "Menu", (200, 200, 200), (RES_X/1.1, RES_Y/1.7 + int(font_size * 4.5)), True)

        if self.key_helper.detect_save_score_press():
            self.main_menu.save_score(self.name_input.text, self.score)



    def draw_pause(self):
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 5))
        text_surface = myfont.render('PAUSE', False, (255, 255, 255))
        self.screen.blit(text_surface, (RES_X / 2 - int(RES_X / 7.7), RES_Y / 2 - int(RES_Y / 20)))

    def draw_boss_prepare(self):
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 6))
        text_surface = myfont.render('PREPARE FOR FIGHT', False, (255, 255, 255))
        self.screen.blit(text_surface, (RES_X / 2 - int(RES_X / 3), RES_Y / 2 - int(RES_Y / 20)))

    def draw_mobs_prepare(self):
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 6))
        text_surface = myfont.render('FIGHTERS INCOMING', False, (255, 255, 255))
        self.screen.blit(text_surface, (RES_X / 2 - int(RES_X / 3), RES_Y / 2 - int(RES_Y / 20)))

    def draw_lives(self):
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 20))
        lives_surface = myfont.render(f'Lives: {int(self.lives)}', False, (255, 255, 255))
        self.screen.blit(lives_surface, (int(RES_X / 40) * 36, int(RES_Y / 40) * 38))

    def draw_kill_count(self, kill_count: int = 0):
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 20))
        lives_surface = myfont.render(f'Kills left: {int(kill_count)}', False, (255, 255, 255))
        self.screen.blit(lives_surface, (int(RES_X / 40) * 34.9, int(RES_Y / 40) * 36))
