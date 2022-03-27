import pygame
from cmd.config.config import (
    SOUND_SHOT,
    SOUND_EXPLOSION_SHORT
)


class SoundHelper:
    def __init__(self):
        self.shot = pygame.mixer.Sound(SOUND_SHOT)
        self.expl_short = pygame.mixer.Sound(SOUND_EXPLOSION_SHORT)

    def sound_shot(self):
        self.shot.play()

    def sound_explosion_short(self):
        self.expl_short.play()
