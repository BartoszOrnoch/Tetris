import pygame

from tetrion import Tetrion

from blocks import BlockI


def print_white_background():
    screen.fill((255, 255, 255))


def print_board():
    for y, row in enumerate(tetrion.board):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (0, 0, 0),
                                 (x*square_size, y*square_size, square_size, square_size), 1)


def print_block():
    for y, row in enumerate(block.state):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (255, 0, 0),
                                 ((x+block.x)*square_size, (y+block.y)*square_size, square_size, square_size))


pygame.init()

a = [[0, 1, 1, 0, 0], [0, 0, 1, 0, 0], [
    0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]

rows = 25
cols = 14
square_size = 40
screen = pygame.display.set_mode((cols*square_size, rows*square_size))

running = True
time = 0
prepare_next = False
tetrion = Tetrion()
block = BlockI()

next_block = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            if block.check_if_on_edge('right'):
                x, y = block.get_coords()
                part = tetrion.get_part(x+1, y)
                if block.can_move(part):
                    block.move_right()

        if keys[pygame.K_LEFT]:
            if block.check_if_on_edge('left'):
                x, y = block.get_coords()
                part = tetrion.get_part(x-1, y)
                if block.can_move(part):
                    block.move_left()

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

        if prepare_next:
            tetrion.update_board(block.state, block.y, block.x)
            if tetrion.check_last_row():
                tetrion.move_row_down()
            #score += 1
            block = BlockI()
            prepare_next = False
        time += 1
        print(f'minelo {time} sekund')

    print_white_background()
    print_board()
    print_block()
    pygame.display.update()
