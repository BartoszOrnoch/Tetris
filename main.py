import pygame

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
    screen.blit(menu_screen, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
        clock.tick(30)


pygame.init()
pygame.font.init()
font = pygame.font.SysFont("comicsansms", 40)
screen = pygame.display.set_mode((sett.WIDTH, sett.HEIGHT))
menu_screen = pygame.Surface((sett.SQUARE_SIZE*12, sett.SQUARE_SIZE*22))
pause_screen = menu = pygame.Surface(
    (sett.SQUARE_SIZE*12, sett.SQUARE_SIZE*22))
game_over_screen = pygame.Surface((sett.SQUARE_SIZE*12, sett.SQUARE_SIZE*22))
clock = pygame.time.Clock()


def main():

    running = True
    is_game_over = False

    prepare_next = False
    tetrion = Tetrion()
    block = blocks.get_random_block()
    next_block = blocks.get_random_block()

    score = 0
    level = 1
    time = 0
    move_time = 0
    move_time_limit = 1000

    try_move_down = False
    try_move_left = False
    try_move_right = False
    try_rotate = False
    drop = False

    main_menu_active = True
    pygame.time.set_timer(26, 100)

    draw.draw_text(menu_screen, 'Press ENTER to start game',
                   sett.COLORS[0], font, 0, 0)
    draw.draw_rectangle(menu_screen, sett.SQUARE_SIZE, sett.SQUARE_SIZE,
                        sett.SQUARE_SIZE*10, sett.SQUARE_SIZE*20)
    draw.draw_text(pause_screen, 'Game is Paused', sett.COLORS[0], font, 0, 0)
    draw.draw_rectangle(pause_screen, sett.SQUARE_SIZE, sett.SQUARE_SIZE,
                        sett.SQUARE_SIZE*10, sett.SQUARE_SIZE*20)

    while running:
        if main_menu_active:
            running = main_menu()
        main_menu_active = False

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
            while prepare_next == False:
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

        draw.fill_surface(screen, sett.COLORS[1])
        draw.draw_squares(tetrion.board, screen)
        draw.draw_squares(block.state, screen, block.x, block.y)
        draw.draw_squares(next_block.state, screen, 17, 5)
        draw.draw_rectangle(screen, sett.SQUARE_SIZE, sett.SQUARE_SIZE,
                            sett.SQUARE_SIZE*10, sett.SQUARE_SIZE*20)
        draw.draw_text(screen, 'NEXT BLOCK:', sett.COLORS[0], font, 12, 4)
        draw.draw_text(screen, f'SCORE: {score}', sett.COLORS[0], font, 12, 8)
        draw.draw_text(screen, f'LEVEL: {level}', sett.COLORS[0], font, 12, 9)
        draw.draw_text(
            screen, f'TIME: {time // 1000} s', sett.COLORS[0], font, 12, 10)
        draw.draw_text(
            screen, f'MOVE TIME: {move_time}', sett.COLORS[0], font, 12, 11)

        is_game_over = tetrion.is_lost()
        if is_game_over:
            print('przegrana')

        pygame.display.update()
        clock.tick(30)


main()
