import pygame
import blocks
import settings as sett
import draw
from tetrion import Tetrion


def main_menu():
    colors = sett.COLORS[2:]
    current_color = colors.pop()
    time = 0
    level = 1
    instructions_surface = draw.get_instruction_surface()
    menu_screen = draw.get_menu_surface(level, current_color)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, level
            if event.type == 26:
                time += 100
                if time == 1000:
                    current_color = colors.pop()
                    if colors == []:
                        colors = sett.COLORS[2:]
                    menu_screen = draw.get_menu_surface(level, current_color)
                    time = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True, level
                if event.key == pygame.K_w:
                    if level < 10:
                        level += 1
                        menu_screen = draw.get_menu_surface(
                            level, current_color)
                if event.key == pygame.K_s:
                    if level > 1:
                        level -= 1
                        menu_screen = draw.get_menu_surface(
                            level, current_color)

        draw.draw_surface(screen, menu_screen, 0, 0)
        draw.draw_surface(screen, instructions_surface, 12, 2)
        draw.draw_rectangle(screen, 1, 1, 10, 20)
        pygame.display.update()
        clock.tick(30)


def pause():
    pause_screen = draw.get_pause_surface()
    instructions_surface = draw.get_instruction_surface()
    draw.draw_surface(screen, pause_screen, 0, 0)
    draw.draw_surface(screen, instructions_surface, 12, 2)
    draw.draw_rectangle(screen, 1, 1, 10, 20)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True
        clock.tick(30)


def game_over(score):
    game_over_screen = draw.get_game_over_surface(score)
    ladderboard_screen = draw.get_ladderboard_surface(score)
    draw.draw_surface(screen, game_over_screen, 0, 0)
    draw.draw_surface(screen, ladderboard_screen, 12, 2)
    draw.draw_rectangle(screen, 1, 1, 10, 20)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        clock.tick(30)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(
    (sett.WIDTH, sett.HEIGHT))


def main():

    running = True
    main_menu_active = True
    pygame.time.set_timer(26, 100)

    while running:
        if main_menu_active:
            running, level = main_menu()
            tetrion = Tetrion()
            block = blocks.get_random_block()
            next_block = blocks.get_random_block()
            prepare_next = False
            score = 0
            time = 0
            move_time = 0
            move_time_limit = 1000 - (level-1)*100
            try_move_down = False
            try_move_left = False
            try_move_right = False
            try_rotate = False
            drop = False
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
            score += 100
            block = next_block
            next_block = blocks.get_random_block()
            prepare_next = False

        score_surface = draw.get_text_surface(f'SCORE: {score}')
        time_surface = draw.get_text_surface(f'TIME: {time // 1000}')
        level_surface = draw.get_text_surface(f'LEVEL: {level}')
        next_block_surface = draw.get_text_surface('next block:')

        draw.fill_surface(screen, sett.COLORS[1])
        draw.draw_squares(tetrion.board, screen)
        draw.draw_squares(block.state, screen, block.x, block.y)
        draw.draw_squares(next_block.state, screen, 17, 5)
        draw.draw_rectangle(screen, 1, 1, 10, 20)
        draw.draw_surface(screen, next_block_surface, 12, 4)
        draw.draw_surface(screen, score_surface, 12, 8)
        draw.draw_surface(screen, level_surface, 12, 9)
        draw.draw_surface(screen, time_surface, 12, 10)

        if tetrion.is_lost():
            running = game_over(score)
            main_menu_active = True

        pygame.display.update()
        clock.tick(30)


main()
