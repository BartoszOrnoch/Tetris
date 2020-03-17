import pygame

from tetrion import tetrion


def get_tetrion_part(i, j):
    return [row[i:i+5] for row in tetrion[j:j+5]]


def can_move(block, tetr_part):
    for i in range(5):
        for j in range(5):
            if block[i][j] and tetr_part[i][j]:
                return False
    return True


def check_last_row():
    pass


def check_if_lost():
    pass


def update_tetrion(block, i, j):
    for row_number, row in enumerate(block):
        for cell_number, cell in enumerate(row):
            if cell:
                tetrion[i+row_number][j+cell_number] = cell


pygame.init()

a = [[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [
    0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]

rows = 25
cols = 14
square_size = 40
screen = pygame.display.set_mode((cols*square_size, rows*square_size))
running = True
coord_x = 0
coord_y = 0

time = 0

print(get_tetrion_part(1, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if coord_x < 9:
                if can_move(a, get_tetrion_part(coord_x + 1, coord_y)):
                    coord_x += 1
                    print('gowno')
        if keys[pygame.K_LEFT]:
            if coord_x > 0:
                if can_move(a, get_tetrion_part(coord_x - 1, coord_y)):
                    coord_x -= 1
                    print('gowno')

    if (pygame.time.get_ticks() // 1000) > time:
        if coord_y < 19:
            if can_move(a, get_tetrion_part(coord_x, coord_y+1)):
                coord_y += 1
            else:
                print(coord_x, coord_y)
                update_tetrion(a, coord_y, coord_x)
                print('xDDD')
                coord_x = 2
                coord_y = 0

        time += 1
        print(f'minelo {time} sekund')

    screen.fill((255, 255, 255))

    for y, row in enumerate(tetrion):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (0, 0, 0),
                                 (x*square_size, y*square_size, square_size, square_size), 1)

    for y, row in enumerate(a):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (255, 0, 0),
                                 ((x+coord_x)*square_size, (y+coord_y)*square_size, square_size, square_size))
    pygame.display.update()
