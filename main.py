import pygame
import blocks
import random

from tetrion import Tetrion


def square_postion(x, y, local_shift_x, local_shift_y):
    return ((x+local_shift_x)*square_size + GLOBAL_SHIFT_X, (y + local_shift_y)*square_size + GLOBAL_SHIFT_Y, square_size, square_size)


def print_white_background():
    screen.fill((255, 255, 255))


def print_board(array2d, local_shift_x=0, local_shift_y=0):
    for y, row in enumerate(array2d):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen, colors[cell], square_postion(x, y, local_shift_x, local_shift_y))


def get_random_block():
    return random.choice([blocks.BlockI(), blocks.BlockJ(), blocks.BlockL(), blocks.BlockO(), blocks.BlockS(), blocks.BlockT(), blocks.BlockZ()])


colors = [(255, 255, 255), (255, 255, 255), (0, 255, 255), (128, 0, 128),
          (255, 165, 0), (0, 0, 255), (0, 128, 0), (255, 0, 0), (255, 255, 0)]

square_size = 40
GLOBAL_SHIFT_X = - square_size
GLOBAL_SHIFT_Y = - square_size*4


pygame.init()

rows = 22
cols = 14

screen = pygame.display.set_mode((cols*square_size, rows*square_size))

running = True
time = 0
score = 0
prepare_next = False
tetrion = Tetrion()
block = get_random_block()
next_block = get_random_block()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if block.check_if_on_edge('right'):
                x, y = block.get_coords()
                part = tetrion.get_part(x+1, y)
                if block.can_move(part):
                    block.move_right()

        if keys[pygame.K_a]:
            if block.check_if_on_edge('left'):
                x, y = block.get_coords()
                part = tetrion.get_part(x-1, y)
                if block.can_move(part):
                    block.move_left()

        if keys[pygame.K_r]:
            x, y = block.get_coords()
            part = tetrion.get_part(x, y)
            if block.can_rotate(part):
                print('nic')
                block.rotate()

        if keys[pygame.K_s]:
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

    if (pygame.time.get_ticks() // 500) > time:

        if block.check_if_on_edge('bottom'):
            x, y = block.get_coords()
            part = tetrion.get_part(x, y+1)
            if block.can_move(part):
                block.move_down()
            else:
                prepare_next = True
        else:
            prepare_next = True
        time += 1
        print(f'minelo {time} sekund')

    if prepare_next:
        tetrion.update_board(block.state, block.y, block.x)
        score += tetrion.remove_rows() ** 2 * 1000
        print(score)
        block = next_block
        next_block = get_random_block()
        prepare_next = False

    print_white_background()
    print_board(tetrion.board)
    print_board(block.state, block.x, block.y)
    pygame.draw.rect(screen, (0, 0, 0),
                     (square_size, square_size, square_size*10, square_size*20), 1)
    # print_block(next_block)

    pygame.display.update()
