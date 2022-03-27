import os
import pygame

GAME_TITLE = 'StarWhats'
RES_X = 1280
RES_Y = 720
SPAWN_RATE = 100
speed = 5
GAME_SPEED_FPS = 60

img_folder = "png"
sounds_folder = "sounds"

SHOT_IMG = os.path.join(img_folder, "shot.png")
BACKGOUND_TILE_IMG = os.path.join(img_folder, "tile_bg.jpg")
BASE_MOB_IMG = os.path.join(img_folder, "x-wing-small-inverted.png")
BASE_PLAYER_IMG = os.path.join(img_folder, "x-wing-small.png")
EXPLOSION_IMAGE = os.path.join(img_folder, "explosion.png")

# CONTROLS
PAUSE_KEY = pygame.K_p
SHOOT_KEY_MAIN = pygame.K_SPACE
FREE_FLIGHT_KEY = pygame.K_LCTRL

# SOUNDS
SOUND_SHOT = os.path.join(sounds_folder, "blaster_shot.ogg")
