import pygame
from cmd.objects.Player import Player
from cmd.objects.BaseMob import BaseMob
from cmd.objects.ObjectPositions import ObjectPositions
from cmd.background.TileBackground import TileBackground
from cmd.helpers.KeyHelper import detect_player_move, detect_player_rotate, detect_shoot

# константы и объект игры
display_size = (1024, 1024)
pygame.init()
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("sw game")

speed = 5
shoot_delay = 0
shot_img = pygame.image.load("png/shot.png")

# основной класс-синглтон, который хранит координаты всех объектов и через который считаем взаимодействия
object_positions = ObjectPositions(screen=screen)

# синглтон игрока - будет один
player = Player(img="png/x-wing-small.png",
                screen=screen,
                object_positions=object_positions)

# объект фона - один
bg = TileBackground(img="png/tile_bg.jpg",
                    screen=screen)

# спавним мобов сколько нужно
for _ in range(3):
    object_positions.add_mob(img="png/x-wing-small-inverted.png",
                             screen=screen,
                             object_positions=object_positions)

clock = pygame.time.Clock()
run = True
while run:
    # 60 фпс
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # считываем нажатия клавиш
    keys = pygame.key.get_pressed()

    # передвижение верх-низ-лево-право
    # delta_x, delta_y, changed, left, right, up, down = detect_player_move(keys, speed)
    # player.get_set_orientation(delta_x, delta_y, changed)

    # передвижение поворот + вперед-назад - определяем по кнопкам
    move_speed, left, right = detect_player_rotate(keys, speed)
    # определяем направление полета
    left, right, up, down = player.get_set_rotation(move_speed, left, right)

    shoot = detect_shoot(keys)
    if shoot:
        # стрельба - спавним новый выстрел раз в 20 фреймов (3 раза в секунду). Выстрел тоже объект
        if shoot_delay <= 0:
            object_positions.add_shot(shot_img, player.orientation)
            shoot_delay = 20

    # обратный отсчет фреймов до след выстрела
    if shoot_delay > 0:
        shoot_delay -= 1

    # двигаем фон
    bg.move(left, right, up, down)

    # двигаем мобов и выстрелы
    object_positions.move_mobs(left, right, up, down)
    object_positions.move_shots()

    # ищем пересечения хитбоксов мобов с игроком и выстрелами
    object_positions.find_collisions()

    # сначала всегда отрисовываем фон, потом сверху все остальное
    bg.draw()

    # отрисовываем игрока и мобов
    object_positions.draw_mobs()
    player.draw()

    pygame.display.update()

pygame.quit()