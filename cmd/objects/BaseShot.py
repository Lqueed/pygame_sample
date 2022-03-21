from cmd.helpers.ObjectHelper import rot_center
import math


class BaseShot:
    """
    Базовый класс для выстрелов - хранит состояние, координаты, угол, скорость и id
    """
    def __init__(self, id, object_positions, img, angle, pos_x, pos_y, screen):
        self.id = id
        self.object_positions = object_positions
        self.img = img
        self.angle = angle
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.screen = screen
        self.speed = 15  # пока хардкод
        self.age = 0

    def move(self):
        """
        Летит строго туда куда запустили, храним угол и скорость
        """
        speed_x = int(math.sin(self.angle * 0.017) * self.speed)
        speed_y = int(math.cos(self.angle * 0.017) * self.speed)

        left = None
        right = None
        up = None
        down = None
        if speed_x > 0:
            left = abs(speed_x)
        elif speed_x < 0:
            right = abs(speed_x)
        if speed_y > 0:
            up = abs(speed_y)
        elif speed_y < 0:
            down = abs(speed_y)

        if left:
            self.pos_x -= left
        if right:
            self.pos_x += right
        if up:
            self.pos_y -= up
        if down:
            self.pos_y += down

        self.age += 1
        self.draw_shot()

    def draw_shot(self):
        self.screen.blit(self.img, (self.pos_x, self.pos_y))