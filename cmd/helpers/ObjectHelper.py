import pygame


# тут общие методы помогайки, касающиеся объектов
def rot_center(image, angle, x, y):
    """
    Повернуть спрайт относительно центра
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect