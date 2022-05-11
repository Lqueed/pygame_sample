from cmd.config.config import (
    RES_X,
    RES_Y,
    GAME_SPEED_FPS
)
import pygame
import time


class BaseStats:
    def __init__(self,
                 screen):
        self.screen = screen
        self.score = 0
        self.time_spent = 0
        self.frame_count = 0
        self.lives = 1

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

    def draw_endgame(self):
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 5))
        text_surface = myfont.render('YOU FUCKED UP', False, (255, 255, 255))
        self.screen.blit(text_surface, (RES_X / 2 - int(RES_X / 3.2), RES_Y / 2 - int(RES_Y / 20)))

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
