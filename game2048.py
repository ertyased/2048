from enum import Enum
from random import choice


class Move(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Game2048:
    def __init__(self):
        self.field = [[0] * 4 for _ in range(4)]
        self.score = 0

    def set_field(self, _field):
        self.field = _field
        self.score = sum(list(map(sum, _field)))

    def get_score(self):
        return self.score

    def get_field(self):
        return self.field

    def transpose(self):
        for i in range(4):
            for j in range(i):
                self.field[i][j], self.field[j][i] = self.field[j][i], self.field[i][j]

    def move(self, move_type: Move):
        if move_type == Move.LEFT:
            for i in range(4):
                row = self.field[i]
                arr = [0] * 4
                j = 0
                for num in row:
                    if num != 0:
                        arr[j] = num
                        j += 1
                self.field[i] = arr
        elif move_type == Move.RIGHT:
            for i in range(4):
                row = self.field[i]
                arr = [0] * 4
                j = 3
                for num in row[::-1]:
                    if num != 0:
                        arr[j] = num
                        j -= 1
                self.field[i] = arr
        elif move_type == Move.DOWN:
            self.transpose()
            self.move(Move.RIGHT)
            self.transpose()
        elif move_type == Move.UP:
            self.transpose()
            self.move(Move.LEFT)
            self.transpose()

        tile = self.choose_empty()
        self.field[tile[0]][tile[1]] = 1

    def choose_empty(self):
        empty_fields = []
        for i in range(4):
            for j in range(4):
                if self.field[i][j] == 0:
                    empty_fields.append([i, j])
        return choice(empty_fields)

    def start(self):
        tile = self.choose_empty()
        self.field[tile[0]][tile[1]] = 1


