import pygame
from cmd.objects.BaseStats import BaseStats
from cmd.objects.Player import Player
from cmd.objects.ObjectPositions import ObjectPositions
from cmd.background.TileBackground import TileBackground
from cmd.helpers.KeyHelper import KeyHelper
from cmd.helpers.SoundHelper import SoundHelper
from cmd.config.config import (
    GAME_TITLE,
    RES_X,
    RES_Y,
    speed,
    SHOT_IMG,
    BACKGOUND_TILE_IMG,
    BASE_MOB_IMG,
    BASE_PLAYER_IMG,
    GAME_SPEED_FPS,
    BOMB_IMG,
)

"""
Все методы содержащие в названии draw - отрисовывают объекты на экране
Все методы содержащие в названии move - просчитывают передвижение объектов
"""


# константы и объект игры
display_size = (RES_X, RES_Y)

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption(GAME_TITLE)

# temp background music
pygame.mixer.music.load("sounds/DuelOfFates.mp3")
pygame.mixer.music.set_volume(1.2)
pygame.mixer.music.play(-1)

shoot_delay = 0
bomb_delay = 0
shot_img = pygame.image.load(SHOT_IMG)
bomb_img = pygame.image.load(BOMB_IMG)

main_stats = BaseStats(screen=screen)
key_helper = KeyHelper()
sound_helper = SoundHelper()

# основной класс-синглтон, который хранит координаты всех объектов и через который считаем взаимодействия
object_positions = ObjectPositions(screen=screen, stats=main_stats, sounds=sound_helper)
stats = object_positions.stats

# синглтон игрока - будет один
# player = Player(img="png/x-wing-small.png",
#                 screen=screen,
#                 object_positions=object_positions)

# объект фона - один
bg = TileBackground(img=BACKGOUND_TILE_IMG,
                    screen=screen)

# спавним мобов сколько нужно
for _ in range(1):
    object_positions.add_mob(img=BASE_MOB_IMG,
                             screen=screen,
                             object_positions=object_positions)

object_positions.add_player(
    Player(img=BASE_PLAYER_IMG,
           screen=screen,
           object_positions=object_positions)
)

clock = pygame.time.Clock()

run = True
pause_game = False
end_game = False

while run:
    clock.tick(GAME_SPEED_FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # считываем нажатия клавиш
    keys = pygame.key.get_pressed()

    if key_helper.detect_esc(keys):
        run = False

    if end_game:
        bg.draw()
        object_positions.draw_all()
        stats.draw_endgame()
        pygame.display.update()
        continue

    if key_helper.detect_pause(keys):
        pause_game = not pause_game

    if pause_game:
        bg.draw()
        object_positions.draw_all()
        stats.draw_pause()
        pygame.display.update()
        continue

    # спавн мобов если кончились
    object_positions.spawn_more_mobs_random()

    # передвижение поворот + вперед-назад - определяем по кнопкам
    move_speed, left, right = key_helper.detect_player_rotate(keys, speed)

    # полет по инерции
    free_flight = key_helper.detect_free_flight(keys)

    # определяем направление полета
    if free_flight:
        left, right, up, down = object_positions.player_obj.get_set_rotation_free_flight(left, right)
    else:
        left, right, up, down = object_positions.player_obj.get_set_rotation(
            move_speed,
            left,
            right,
            object_positions.player_obj.destroyed
        )

    shoot = key_helper.detect_shoot(keys)
    shot_type = object_positions.get_player_shot_type()
    if shoot:
        # стрельба - спавним новый выстрел раз в 20 фреймов (3 раза в секунду). Выстрел тоже объект
        if shoot_delay <= 0:
            object_positions.add_shot(object_positions.player_obj.orientation, shot_type=shot_type)
            shoot_delay = 20

    bomb = key_helper.detect_bomb_drop(keys)
    if bomb:
        if bomb_delay <= 0:
            object_positions.add_bomb(bomb_img)
            bomb_delay = 120

    # обратный отсчет фреймов до след выстрела
    if shoot_delay > 0:
        shoot_delay -= 1
    if bomb_delay > 0:
        bomb_delay -= 1

    # двигаем фон
    bg.move(left, right, up, down)

    # сначала всегда отрисовываем фон, потом сверху все остальное
    bg.draw()

    object_positions.del_too_far_objects()

    # двигаем мобов и выстрелы
    object_positions.move_objects(left, right, up, down)
    object_positions.move_shots()

    # ищем пересечения хитбоксов мобов с игроком и выстрелами
    object_positions.find_collisions()

    # отрисовываем игрока и мобов
    object_positions.draw_all()

    if object_positions.player_obj.destroyed:
        end_game = True

    stats.increase_time()
    pygame.display.update()

pygame.quit()