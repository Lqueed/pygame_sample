import pygame
import random


# тут общие методы помогайки, касающиеся объектов
def rot_center(image, angle, x, y):
    """
    Повернуть спрайт относительно центра
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect


def random_fn(chance: int = 100):
    rnd = random.randint(0, chance)
    if rnd == 0:
        return True
    return False