import pygame

from tetrion import Tetrion

import blocks


def print_white_background():
    screen.fill((255, 255, 255))


def print_board():
    for y, row in enumerate(tetrion.board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (0, 0, 0),
                                 (x*square_size, y*square_size, square_size, square_size), 1)


def print_block():
    for y, row in enumerate(block.state):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (255, 0, 0),
                                 ((x+block.x)*square_size, (y+block.y)*square_size, square_size, square_size))


pygame.init()

rows = 25
cols = 14
square_size = 40
screen = pygame.display.set_mode((cols*square_size, rows*square_size))

running = True
time = 0
score = 0
prepare_next = False
tetrion = Tetrion()
block = blocks.BlockO()
next_block = False

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
        if tetrion.check_last_row():
            tetrion.move_row_down()
            #score += 1
        block = blocks.BlockI()
        prepare_next = False

    print_white_background()
    print_board()
    print_block()
    pygame.display.update()
