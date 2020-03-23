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


def draw_surface(surface, text_surface, position_x, position_y, position_in_squares=True):
    if position_in_squares:
        multiplier = sett.SQUARE_SIZE
    else:
        multiplier = 1
    surface.blit(text_surface, (position_x *
                                multiplier, position_y*multiplier))


def get_text_surface(text, color=sett.COLORS[0], font_size=25):
    pygame.font.init()
    font = pygame.font.SysFont("small pixel", font_size)
    return font.render(text, True, color)


def get_space(surface):
    return (surface.get_rect().width, surface.get_rect().height)


def get_instruction_surface():
    instruction_screen = pygame.Surface(
        (sett.TEXT_SURFACE_WIDTH, sett.TEXT_SURFACE_HEIGHT))
    ins1 = get_text_surface('in game:')
    ins2 = get_text_surface('A - block left')
    ins3 = get_text_surface('d - block right')
    ins4 = get_text_surface('s - block down')
    ins5 = get_text_surface('r - block rotate')
    ins6 = get_text_surface('p - pause/unpause')
    ins7 = get_text_surface('menu')
    ins8 = get_text_surface('w - level up')
    ins9 = get_text_surface('s - level down')

    draw_surface(instruction_screen, ins1, 0, 0)
    draw_surface(instruction_screen, ins2, 0, 1)
    draw_surface(instruction_screen, ins3, 0, 2)
    draw_surface(instruction_screen, ins4, 0, 3)
    draw_surface(instruction_screen, ins5, 0, 4)
    draw_surface(instruction_screen, ins6, 0, 5)
    draw_surface(instruction_screen, ins7, 0, 7)
    draw_surface(instruction_screen, ins8, 0, 8)
    draw_surface(instruction_screen, ins9, 0, 9)
    return instruction_screen


def get_menu_surface(level, color):
    menu_screen = pygame.Surface(
        (sett.TEXT_SURFACE_WIDTH, sett.TEXT_SURFACE_HEIGHT))
    level_surface = get_text_surface(f'level: {level}')
    enter_surface = get_text_surface(f'press space to start', color)
    level_x, level_y = get_space(level_surface)
    enter_x, enter_y = get_space(enter_surface)
    draw_surface(menu_screen, enter_surface, (sett.TEXT_SURFACE_WIDTH - enter_x)/2,
                 (sett.TEXT_SURFACE_HEIGHT - enter_y)/2, position_in_squares=False)
    draw_surface(menu_screen, level_surface, (sett.TEXT_SURFACE_WIDTH - level_x)/2,
                 (sett.TEXT_SURFACE_HEIGHT - level_y)/2 + sett.SQUARE_SIZE, position_in_squares=False)
    return menu_screen


def get_pause_surface():
    pause_screen = pygame.Surface(
        (sett.TEXT_SURFACE_WIDTH, sett.TEXT_SURFACE_HEIGHT))
    pause_text = get_text_surface(f'Game paused')
    pause_x, pause_y = get_space(pause_text)
    draw_surface(pause_screen, pause_text, (sett.TEXT_SURFACE_WIDTH - pause_x)/2,
                 (sett.TEXT_SURFACE_HEIGHT - pause_y)/2, position_in_squares=False)
    return pause_screen


def get_game_over_surface(score):
    game_over_screen = pygame.Surface(
        (sett.TEXT_SURFACE_WIDTH, sett.TEXT_SURFACE_HEIGHT))
    game_over_text = get_text_surface('game over')
    score_text = get_text_surface(f'your score: {score}')
    restart_text = get_text_surface('press space to restart')
    game_over_x, game_over_y = get_space(game_over_text)
    score_x, score_y = get_space(score_text)
    restart_x, restart_y = get_space(restart_text)
    draw_surface(game_over_screen, game_over_text, (sett.TEXT_SURFACE_WIDTH - game_over_x)/2,
                 (sett.TEXT_SURFACE_HEIGHT - game_over_y)/2, position_in_squares=False)
    draw_surface(game_over_screen, score_text, (sett.TEXT_SURFACE_WIDTH - score_x)/2,
                 (sett.TEXT_SURFACE_HEIGHT - score_y)/2 + sett.SQUARE_SIZE, position_in_squares=False)
    draw_surface(game_over_screen, restart_text, (sett.TEXT_SURFACE_WIDTH - restart_x)/2,
                 (sett.TEXT_SURFACE_HEIGHT - restart_y)/2 + sett.SQUARE_SIZE*2, position_in_squares=False)
    return game_over_screen


def get_ladderboard_surface(score):
    with open('ladderboard.txt', 'r') as file:
        ladderboard = [int(line.strip('\n')) for line in file]
        if min(ladderboard) < score:
            ladderboard.pop()
            ladderboard.append(score)
            ladderboard.sort(reverse=True)
            update_ladderboard = True
    if update_ladderboard:
        with open('ladderboard.txt', 'w') as file:
            for highscore in ladderboard:
                file.write(f'{highscore}\n')
    ladderboard_menu = pygame.Surface(
        (sett.TEXT_SURFACE_WIDTH, sett.TEXT_SURFACE_HEIGHT))
    highscores_text = get_text_surface('highscores:')
    draw_surface(ladderboard_menu, highscores_text, 0, 0)
    for index, highscore in enumerate(ladderboard, 2):
        score_surface = get_text_surface(f'{index-1}.  {highscore}')
        draw_surface(ladderboard_menu, score_surface, 0, index)
    return ladderboard_menu
