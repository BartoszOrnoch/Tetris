import pygame
import settings as sett


def square_coords(x, y, local_shift_x, local_shift_y, global_x=sett.GLOBAL_SHIFT_X, global_y=sett.GLOBAL_SHIFT_Y):
    return ((x+local_shift_x)*sett.SQUARE_SIZE + global_x, (y + local_shift_y)*sett.SQUARE_SIZE + global_y, sett.SQUARE_SIZE, sett.SQUARE_SIZE)


def draw_squares(array2d, surface, local_shift_x=0, local_shift_y=0):
    for y, row in enumerate(array2d):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    surface, sett.COLORS[cell], square_coords(x, y, local_shift_x, local_shift_y))


def draw_rectangle(surface, x, y, width, height):
    pygame.draw.rect(surface, (255, 255, 255),
                     (x, y, width, height), 2)


def fill_surface(surface, color):
    surface.fill(color)


def draw_text(surface, text, color, font, position_x, position_y):
    surface.blit(font.render(text, True, color), (position_x *
                                                  sett.SQUARE_SIZE, position_y*sett.SQUARE_SIZE))
