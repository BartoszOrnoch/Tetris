class BlockI:

    rotations = [[[0, 0, 2, 0, 0], [0, 0, 2, 0, 0], [
        0, 0, 2, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
            0, 2, 2, 2, 2], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [
            0, 0, 2, 0, 0], [0, 0, 2, 0, 0], [0, 0, 2, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
            2, 2, 2, 2, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]

    def __init__(self):
        self.x = 6
        self.y = 1
        self.current_rotation = 0
        self.next_rotation = 1
        self.state = self.rotations[self.current_rotation]

    def can_move(self, tetr_part):
        for i in range(5):
            for j in range(5):
                if self.state[i][j] and tetr_part[i][j]:
                    return False
        return True

    def check_if_on_edge(self, edge):
        if edge == 'left':
            return self.x > 0
        if edge == 'right':
            return self.x < 9
        if edge == 'bottom':
            return self.y < 22

    def can_rotate(self, tetr_part):
        for i in range(5):
            for j in range(5):
                if self.rotations[self.next_rotation][i][j] and tetr_part[i][j]:
                    return False
        return True

    def rotate(self):
        self.state = self.rotations[self.next_rotation]
        if self.next_rotation == 3:
            self.next_rotation = 0
        else:
            self.next_rotation += 1

    def get_coords(self):
        return (self.x, self.y)

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_down(self):
        self.y += 1


class BlockT(BlockI):
    rotations = [[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
        0, 3, 3, 3, 0], [0, 0, 3, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 3, 0, 0], [0, 3, 3, 0, 0],
            [0, 0, 3, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 3, 0, 0], [0, 3, 3, 3, 0],
            [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 3, 0, 0], [0, 0, 3, 3, 0],
            [0, 0, 3, 0, 0], [0, 0, 0, 0, 0]]
    ]


class BlockL(BlockI):
    rotations = [[[0, 0, 0, 0, 0], [0, 0, 4, 0, 0], [
        0, 0, 4, 0, 0], [0, 0, 4, 4, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 4, 4, 4, 0],
            [0, 4, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 4, 4, 0, 0], [0, 0, 4, 0, 0],
            [0, 0, 4, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 4, 0], [0, 4, 4, 4, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]


class BlockJ(BlockI):
    rotations = [[[0, 0, 0, 0, 0], [0, 0, 5, 0, 0], [
        0, 0, 5, 0, 0], [0, 5, 5, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 5, 0, 0, 0], [0, 5, 5, 5, 0],
            [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 5, 5, 0], [0, 0, 5, 0, 0],
            [0, 0, 5, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 5, 5, 5, 0], [0, 0, 0, 5, 0], [0, 0, 0, 0, 0]]]


class BlockS(BlockI):
    rotations = [[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
        0, 0, 6, 6, 0], [0, 6, 6, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 6, 0, 0, 0], [0, 6, 6, 0, 0],
            [0, 0, 6, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 6, 6, 0], [0, 6, 6, 0, 0],
            [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 6, 0, 0], [0, 0, 6, 6, 0], [0, 0, 0, 6, 0], [0, 0, 0, 0, 0]]]


class BlockZ(BlockI):
    rotations = [[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
        0, 7, 7, 0, 0], [0, 0, 7, 7, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 7, 0, 0], [0, 7, 7, 0, 0],
            [0, 7, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 7, 7, 0, 0], [0, 0, 7, 7, 0],
            [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 0, 0, 7, 0], [0, 0, 7, 7, 0], [0, 0, 7, 0, 0], [0, 0, 0, 0, 0]]]


class BlockO(BlockI):
    rotations = [[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
        0, 0, 8, 8, 0], [0, 0, 8, 8, 0], [0, 0, 0, 0, 0]]]

    def can_rotate(self, part):
        return False
