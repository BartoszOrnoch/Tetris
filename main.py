import pygame
import blocks
import random

from tetrion import Tetrion


def square_coords(x, y, local_shift_x, local_shift_y):
    return ((x+local_shift_x)*SQUARE_SIZE + GLOBAL_SHIFT_X, (y + local_shift_y)*SQUARE_SIZE + GLOBAL_SHIFT_Y, SQUARE_SIZE, SQUARE_SIZE)


def print_white_background():
    screen.fill((0, 0, 0))


def draw_squares(array2d, local_shift_x=0, local_shift_y=0):
    for y, row in enumerate(array2d):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen, COLORS[cell], square_coords(x, y, local_shift_x, local_shift_y))


def get_random_block():
    return random.choice([blocks.BlockI(), blocks.BlockJ(), blocks.BlockL(), blocks.BlockO(), blocks.BlockS(), blocks.BlockT(), blocks.BlockZ()])


def draw_text(text, postion_x, postion_y):
    screen.blit(font.render(
        text, True, COLORS[0]), (postion_x*SQUARE_SIZE, postion_y*SQUARE_SIZE))


def pause():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                return True
        pygame.display.update()


COLORS = [(255, 255, 255), (0, 0, 0), (0, 255, 255), (128, 0, 128),
          (255, 165, 0), (0, 0, 255), (0, 128, 0), (255, 0, 0), (255, 255, 0)]
SQUARE_SIZE = 40
GLOBAL_SHIFT_X = - SQUARE_SIZE
GLOBAL_SHIFT_Y = - SQUARE_SIZE*4
WIDTH = SQUARE_SIZE * 21
HEIGHT = SQUARE_SIZE * 22

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("comicsansms", 40)


def main():

    running = True

    prepare_next = False
    tetrion = Tetrion()
    block = get_random_block()
    next_block = get_random_block()
    clock = pygame.time.Clock()

    time = 0
    score = 0
    level = 1

    try_move_down = False
    try_move_left = False
    try_move_right = False
    try_rotate = False

    block_down_event = pygame.time.set_timer(25, 1000 - level*100)
    pygame.time.set_timer(26, 1000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == 26:
                time += 1

            if event.type == 25:
                if block.check_if_on_edge('bottom'):
                    x, y = block.get_coords()
                    part = tetrion.get_part(x, y+1)
                    if block.can_move(part):
                        block.move_down()
                    else:
                        prepare_next = True
                else:
                    prepare_next = True

            keys = pygame.key.get_pressed()

            if keys[pygame.K_p]:
                running = pause()

            if keys[pygame.K_d]:
                if block.check_if_on_edge('right'):
                    x, y = block.get_coords()
                    part = tetrion.get_part(x+1, y)
                    if block.can_move(part):
                        block.move_right()
                        print(block.get_coords())
                break

            elif keys[pygame.K_a]:
                if block.check_if_on_edge('left'):
                    x, y = block.get_coords()
                    part = tetrion.get_part(x-1, y)
                    if block.can_move(part):
                        block.move_left()
                        print(block.get_coords())
                break

            elif keys[pygame.K_r]:
                x, y = block.get_coords()
                part = tetrion.get_part(x, y)
                if block.can_rotate(part):
                    block.rotate()
                break

            elif keys[pygame.K_s]:
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

        if prepare_next:
            tetrion.update_board(block.state, block.y, block.x)
            score += tetrion.remove_rows() ** 2 * 1000
            block = next_block
            next_block = get_random_block()
            prepare_next = False
            level += 1
            block_down_event = pygame.time.set_timer(25, 1000 - level*100)

        print_white_background()
        draw_squares(tetrion.board)
        draw_squares(block.state, block.x, block.y)
        draw_squares(next_block.state, 17, 5)
        pygame.draw.rect(screen, (255, 255, 255),
                         (SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE*10, SQUARE_SIZE*20), 2)
        draw_text('NEXT BLOCK:', 12, 4)
        draw_text(f'SCORE: {score}', 12, 8)
        draw_text(f'LEVEL: {level}', 12, 9)
        draw_text(f'TIME: {time}', 12, 10)
        # print_block(next_block)

        pygame.display.update()
        clock.tick(60)


main()
