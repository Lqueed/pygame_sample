import sys
from cmd.config.config import *
import pygame

# помощник для отрисовки разного рода надписей.

COLOR_INACTIVE = (180,180,180)
COLOR_ACTIVE = (240,240,240)

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


class InputBox:
    def __init__(self, x, y, w, h, screen, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font = pygame.font.Font(resource_path(os.path.join('cmd/fonts', 'Rexagus.ttf')), int(RES_Y/30))
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.screen = screen

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)