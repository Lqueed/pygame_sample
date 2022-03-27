import pygame
from cmd.config.config import (
    SOUND_SHOT,
)


class SoundHelper:
    def __init__(self):
        self.shot = pygame.mixer.Sound(SOUND_SHOT)

    def sound_shot(self):
        self.shot.play()
