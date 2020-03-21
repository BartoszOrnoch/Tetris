import pygame
import random
import blocks
import settings as sett
import draw
from tetrion import Tetrion


def pause():

    screen.blit(pause_screen, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True
        clock.tick(30)


def main_menu():
    def get_space(surface):
        return (surface.get_rect().width, surface.get_rect().height)

    def update_level():
        level_surface = font.render(
            f'LEVEL: {level}', True, sett.COLORS[0], sett.COLORS[1])
        level_x, level_y = get_space(level_surface)
        draw.draw_rectangle(menu_screen, (sett.TEXT_SURFACE_WIDTH - level_x)/2 * 0.9,
                            (sett.TEXT_SURFACE_HEIGHT - level_y)/2 + sett.SQUARE_SIZE, level_x * 1.2, level_y, position_in_squares=False, border=0, color=sett.COLORS[1])

        draw.draw_text(menu_screen, level_surface, (sett.TEXT_SURFACE_WIDTH - level_x)/2,
                       (sett.TEXT_SURFACE_HEIGHT - level_y)/2 + sett.SQUARE_SIZE, position_in_squares=False)

    def update_enter_game(color):
        enter_game_text = 'press ENTER to start'
        enter_surface = font.render(
            enter_game_text, True, color)
        enter_x, enter_y = get_space(enter_surface)
        draw.draw_text(menu_screen, enter_surface, (sett.TEXT_SURFACE_WIDTH - enter_x)/2,
                       (sett.TEXT_SURFACE_HEIGHT - enter_y)/2, position_in_squares=False)
    level = 1
    colors = sett.COLORS[2:]
    time = 0
    update_enter_game(colors.pop())
    update_level()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, level
            if event.type == 26:
                time += 100
                if time == 1000:
                    if colors == []:
                        colors = sett.COLORS[2:]
                    update_enter_game(colors.pop())
                    time = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True, level
                if event.key == pygame.K_w:
                    if level < 10:
                        level += 1
                        update_level()
                if event.key == pygame.K_s:
                    if level > 1:
                        level -= 1
                        update_level()

        screen.blit(menu_screen, (0, 0))
        draw.draw_rectangle(menu_screen, 1, 1, 10, 20)
        pygame.display.update()
        clock.tick(30)


def game_over():
    screen.blit(game_over_screen, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    return True
        clock.tick(30)


pygame.init()
pygame.font.init()
font = pygame.font.SysFont("small pixel", 25)
screen = pygame.display.set_mode(
    (sett.WIDTH, sett.HEIGHT))
menu_screen = pygame.Surface(
    (sett.TEXT_SURFACE_WIDTH, sett.TEXT_SURFACE_HEIGHT))
pause_screen = pygame.Surface(
    (sett.TEXT_SURFACE_WIDTH, sett.TEXT_SURFACE_HEIGHT))
game_over_screen = pygame.Surface(
    (sett.TEXT_SURFACE_WIDTH, sett.TEXT_SURFACE_HEIGHT))
clock = pygame.time.Clock()


def main():

    running = True
    main_menu_active = True
    restart = True

    pygame.time.set_timer(26, 100)

    while running:
        if main_menu_active:
            running, level = main_menu()
            main_menu_active = False

        if restart:
            tetrion = Tetrion()
            block = blocks.get_random_block()
            next_block = blocks.get_random_block()
            prepare_next = False
            score = 0
            time = 0
            move_time = 0
            move_time_limit = 1000
            try_move_down = False
            try_move_left = False
            try_move_right = False
            try_rotate = False
            drop = False
            restart = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == 26:
                time += 100
                move_time += 100
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    try_move_left = True
                elif event.key == pygame.K_d:
                    try_move_right = True
                elif event.key == pygame.K_s:
                    try_move_down = True
                elif event.key == pygame.K_p:
                    running = pause()
                elif event.key == pygame.K_r:
                    try_rotate = True
                elif event.key == pygame.K_SPACE:
                    drop = True

        if move_time == move_time_limit:
            try_move_down = True

        if try_move_right:
            if block.check_if_on_edge('right'):
                x, y = block.get_coords()
                part = tetrion.get_part(x+1, y)
                if block.can_move(part):
                    block.move_right()
                    print(block.get_coords())
            try_move_right = False

        if try_move_left:
            if block.check_if_on_edge('left'):
                x, y = block.get_coords()
                part = tetrion.get_part(x-1, y)
                if block.can_move(part):
                    block.move_left()
                    print(block.get_coords())
            try_move_left = False

        if drop:
            while not prepare_next:
                if block.check_if_on_edge('bottom'):
                    x, y = block.get_coords()
                    part = tetrion.get_part(x, y+1)
                    if block.can_move(part):
                        block.move_down()
                    else:
                        prepare_next = True
                else:
                    prepare_next = True
            drop = False
            move_time = 0

        if try_move_down:
            if block.check_if_on_edge('bottom'):
                x, y = block.get_coords()
                part = tetrion.get_part(x, y+1)
                if block.can_move(part):
                    block.move_down()
                else:
                    prepare_next = True
            else:
                prepare_next = True
            try_move_down = False
            move_time = 0

        if try_rotate:
            x, y = block.get_coords()
            part = tetrion.get_part(x, y)
            if block.can_rotate(part):
                block.rotate()
            try_rotate = False

        if prepare_next:
            tetrion.update_board(block.state, block.y, block.x)
            score += tetrion.remove_rows() ** 2 * 1000
            block = next_block
            next_block = blocks.get_random_block()
            prepare_next = False
            level += 1

        score_surface = font.render(f'SCORE: {score}', True, sett.COLORS[0])
        time_surface = font.render(
            f'TIME: {time // 1000} s', True, sett.COLORS[0])
        level_surface = font.render(f'LEVEL: {level}', True, sett.COLORS[0])

        draw.fill_surface(screen, sett.COLORS[1])
        draw.draw_squares(tetrion.board, screen)
        draw.draw_squares(block.state, screen, block.x, block.y)
        draw.draw_squares(next_block.state, screen, 17, 5)
        draw.draw_rectangle(screen, 1, 1, 10, 20)
        draw.draw_text(screen, level_surface, 12, 4)
        draw.draw_text(screen, score_surface, 12, 8)
        draw.draw_text(screen, level_surface, 12, 9)
        draw.draw_text(screen, time_surface, 12, 10)
        # draw.draw_text(screen, f'MOVE TIME: {move_time}', font, 12, 11)

        if tetrion.is_lost():
            running = game_over()
            restart = True

        pygame.display.update()
        clock.tick(30)


main()
