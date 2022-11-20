import os
import sys
import pygame

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

GAME_TITLE = 'StarWhats'
RES_X = 1280
RES_Y = 720
SPAWN_RATE = 100
speed = 5
GAME_SPEED_FPS = 60
AGGRESIVE_DISTANSE = 300
TURRET_AGGRESIVE_DISTANSE = 500
MOB_SPEED = 4
SATTELITE_SPEED = 6
PLAYER_ROTATE_SPEED = 3
BOMB_EXPLOSION_RADIUS = 30
ARROWS_TO_MOB = True
SHOT_SPEED = 15
POWER_SHOT_SPEED = 20
BONUS_SPAWN_CHANCE = 10
GROUP_DISTANCE = 50
MINIMAP = 1
TURRET_SHOOT_DELAY = 120
TURRET_SHOT_SPEED = 5
ROCKET_TURRET_SHOOT_DELAY = 360
ROCKET_SHOT_SPEED = 5
SHOT_BONUS_TIME = 1800
PLAYER_LIVES = 2
RESPAWN_DELAY = 120
KILL_COUNT_FOR_BOSS = 1

img_folder = "png"
sounds_folder = "sounds"

#IMAGES
SHOT_IMG = resource_path(os.path.join(img_folder, "shot.png"))
POWER_SHOT_IMG = resource_path(os.path.join(img_folder, "shot_yellow.png"))
BACKGOUND_TILE_IMG = resource_path(os.path.join(img_folder, "tile_bg_blue.jpg"))
BASE_MOB_IMG = resource_path(os.path.join(img_folder, "x-wing-small-inverted.png"))
BIG_MOB_IMG = resource_path(os.path.join(img_folder, "enemy_mid.png"))
SATTELITE_MOB_IMAGE = resource_path(os.path.join(img_folder, "sattelite.png"))
BASE_PLAYER_IMG = resource_path(os.path.join(img_folder, "x-wing-small.png"))
EXPLOSION_IMAGE = resource_path(os.path.join(img_folder, "explosion.png"))
BOMB_IMG = resource_path(os.path.join(img_folder, "bomb.png"))
BONUS_IMG = resource_path(os.path.join(img_folder, "bonus.png"))
DOUBLE_BONUS_IMG = resource_path(os.path.join(img_folder, "double_bonus.png"))
STAR_DESTROYER_IMG = resource_path(os.path.join(img_folder, "star_destroyer.png"))
CORVETTE_IMG = resource_path(os.path.join(img_folder, "corvette.png"))
TURRET_PNG = resource_path(os.path.join(img_folder, "tur.png"))
ROCKET_TURRET_PNG = resource_path(os.path.join(img_folder, "rocket_tur.png"))
ROCKET_IMG = resource_path(os.path.join(img_folder, "rocket.png"))
LIFE_BONUS_IMG = resource_path(os.path.join(img_folder, "lifebonus.png"))

# CONTROLS
PAUSE_KEY = pygame.K_p
SHOOT_KEY_MAIN = pygame.K_SPACE
FREE_FLIGHT_KEY = pygame.K_z
BOMB_KEY = pygame.K_x

# SOUNDS
SOUND_SHOT = resource_path(os.path.join(sounds_folder, "blaster_shot.ogg"))
SOUND_EXPLOSION_SHORT = resource_path(os.path.join(sounds_folder, "explosion_short.ogg"))
SOUND_BOMB_EXPLOSION = resource_path(os.path.join(sounds_folder, "bomb_explosion.ogg"))
