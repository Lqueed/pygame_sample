import os
import pygame

GAME_TITLE = 'StarWhats'
RES_X = 1280
RES_Y = 720
SPAWN_RATE = 100
speed = 5
GAME_SPEED_FPS = 60
AGGRESIVE_DISTANSE = 300
MOB_SPEED = 4
PLAYER_ROTATE_SPEED = 3
ARROWS_TO_MOB = True

img_folder = "png"
sounds_folder = "sounds"

#IMAGES
SHOT_IMG = os.path.join(img_folder, "shot.png")
BACKGOUND_TILE_IMG = os.path.join(img_folder, "tile_bg_blue.jpg")
BASE_MOB_IMG = os.path.join(img_folder, "x-wing-small-inverted.png")
BASE_PLAYER_IMG = os.path.join(img_folder, "x-wing-small.png")
EXPLOSION_IMAGE = os.path.join(img_folder, "explosion.png")
BOMB_IMG = os.path.join(img_folder, "bomb.png")

# CONTROLS
PAUSE_KEY = pygame.K_p
SHOOT_KEY_MAIN = pygame.K_SPACE
FREE_FLIGHT_KEY = pygame.K_LCTRL
BOMB_KEY = pygame.K_LALT

# SOUNDS
SOUND_SHOT = os.path.join(sounds_folder, "blaster_shot.ogg")
SOUND_EXPLOSION_SHORT = os.path.join(sounds_folder, "explosion_short.ogg")
