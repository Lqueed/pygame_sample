import sys
from config.config import *
import pygame

# помощник для отрисовки разного рода надписей.

# отрисовка текста в главном меню
def draw_text(
        screen,
        font,
        text,
        color: tuple = (255, 255, 255),
        place: tuple = (RES_X/2, RES_Y/2),
        highlight_on_hover: bool = False,
    ):
    textbox = font.render(text, True, color)
    place_coords = textbox.get_rect(center=place)
    mouse = pygame.mouse.get_pos()
    # при наведении мыши подсвечиваем текст
    if highlight_on_hover and mouse:
        if (place_coords[0] <= mouse[0] <= place_coords[0] + place_coords[2]) and \
                place_coords[1] <= mouse[1] <= place_coords[1] + place_coords[3]:
            color = (255, 255, 255)
        textbox = font.render(text, True, color)
        place_coords = textbox.get_rect(center=place)
    screen.blit(textbox, place_coords)
    return place_coords