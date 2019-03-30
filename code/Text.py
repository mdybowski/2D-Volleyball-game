import pygame
import pymunk
import pymunk.pygame_util


class Text:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    SIZE = 100
    MAIN_FONT = "res/fonts/BKANT.ttf"

    def __init__(self, font_source, scale_factor, text_color, text, text_pos_x=0, text_pos_y=0):
        main_font = pygame.font.Font(font_source, int(Text.SIZE * scale_factor))
        self.text_surf = main_font.render(text, True, text_color)
        self.text_size = pymunk.Vec2d(self.text_surf.get_width(), self.text_surf.get_height())
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = (text_pos_x, text_pos_y)

    def to_draw(self):
        return self.text_surf, self.text_rect

    def set_text_center(self, text_pos):
        self.text_rect.center = text_pos