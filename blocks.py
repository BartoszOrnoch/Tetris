class BlockI:

    rotations = {0: [[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [
        0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]],
    }

    def __init__(self):
        self.x = 2
        self.y = 0
        self.state = self.rotations[0]

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
            return self.y < 19

    def get_coords(self):
        return (self.x, self.y)

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_down(self):
        self.y += 1
