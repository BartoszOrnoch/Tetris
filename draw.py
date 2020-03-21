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


def draw_rectangle(surface, x, y, width, height, position_in_squares=True, color=sett.COLORS[0], border=2):
    if position_in_squares:
        multiplier = sett.SQUARE_SIZE
    else:
        multiplier = 1
    pygame.draw.rect(surface, color,
                     (x*multiplier, y*multiplier, width*multiplier, height*multiplier), border)


def fill_surface(surface, color):
    surface.fill(color)


def draw_text(surface, text_surface, position_x, position_y, color=sett.COLORS[0], position_in_squares=True):
    if position_in_squares:
        multiplier = sett.SQUARE_SIZE
    else:
        multiplier = 1
    surface.blit(text_surface, (position_x *
                                multiplier, position_y*multiplier))
