from enum import Enum
from random import choice
import math

class Move(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Game2048:
    def __init__(self):
        self.field = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.ended = False

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
        if self.ended:
            return
        prev_state = self.field.copy()
        if move_type == Move.LEFT:
            for i in range(4):
                row = self.field[i]
                arr = [0] * 4
                j = 0
                for num in row:
                    if num != 0:
                        arr[j] = num
                        j += 1
                for i1 in range(3):
                    if arr[i1] == arr[i1 + 1]:
                        self.score += arr[i1] // 2
                        arr[i1] *= 2
                        arr[i1 + 1] = 0
                        i1 += 1
                arr_new = [0] * 4
                j = 0
                for num in arr:
                    if num != 0:
                        arr_new[j] = num
                        j += 1
                self.field[i] = arr_new
        elif move_type == Move.RIGHT:
            for i in range(4):
                row = self.field[i]
                arr = [0] * 4
                j = 3
                for num in row[::-1]:
                    if num != 0:
                        arr[j] = num
                        j -= 1
                for i1 in range(3, -1, -1):
                    if arr[i1] == arr[i1 - 1]:
                        self.score += arr[i1] // 2
                        arr[i1] *= 2
                        arr[i1 - 1] = 0
                        i1 -= 1
                arr_new = [0] * 4
                j = 3
                for num in arr[::-1]:
                    if num != 0:
                        arr_new[j] = num
                        j -= 1
                self.field[i] = arr_new
        elif move_type == Move.DOWN:
            self.transpose()
            self.move(Move.RIGHT)
            self.transpose()
            return
        elif move_type == Move.UP:
            self.transpose()
            self.move(Move.LEFT)
            self.transpose()
            return
        if self.field == prev_state:
            self.ended = True
            return
        self.create_new()

    def check_lose(self):
        for i in range(4):
            for j in range(4):
                if self.field[i][j] == 0:
                    return
                if i != 0 and self.field[i][j] == self.field[i - 1][j]:
                    return
                if j != 0 and self.field[i][j] == self.field[i][j - 1]:
                    return
                if i != 3 and self.field[i][j] == self.field[i + 1][j]:
                    return
                if j != 3 and self.field[i][j] == self.field[i][j + 1]:
                    return
        self.ended = True

    def is_ended(self):
        return self.ended

    def get_field_as_array(self):
        res = []
        for i in range(4):
            for j in range(4):
                res.append(self.field[i][j])
        return res

    def choose_empty(self):
        empty_fields = []
        for i in range(4):
            for j in range(4):
                if self.field[i][j] == 0:
                    empty_fields.append([i, j])
        if len(empty_fields) == 0:
            return [-1, -1]
        return choice(empty_fields)

    def create_new(self):
        self.check_lose()
        tile = self.choose_empty()
        if tile == [-1, -1]:
            self.ended = True
            return
        self.score += 1
        self.field[tile[0]][tile[1]] = 1

    def start(self):
        self.create_new()

    def __str__(self):
        result = ""
        for i in self.field:
            result += "\t".join(map(str, i))
            result += "\n"
        return result

