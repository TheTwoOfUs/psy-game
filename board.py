from random import random


class Board:
    hidden = []   # Hidden board
    visible = []  # Visible board
    mask = []     # Mask used for hover

    difficulty = [
        {"size": 4,
         "clickable": 5},
        {"size": 6,
         "clickable": 10},
        {"size": 8,
         "clickable": 15}
    ]

    def __init__(self, selected):
        self.SIZE = (self.difficulty[selected])["size"]
        self.clickable = (self.difficulty[selected])["clickable"]

        self.tile_size = 384 / self.SIZE

        for i in range(self.SIZE):
            self.hidden.append([])
            self.visible.append([])
            self.mask.append([])
            for j in range(self.SIZE):
                self.hidden[i].append(0)
                self.visible[i].append(0)
                self.mask[i].append(0)

    def generate(self):
        coords = []
        i = 0

        while i < self.clickable:
            x = int(random() * self.SIZE)
            y = int(random() * self.SIZE)
            if (x, y) not in coords:
                coords.append((x, y))
                i += 1

        for (x, y) in coords:
            self.hidden[x][y] = 1

    def clear_visible(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                self.visible[i][j] = 0

    def is_correct_move(self, x, y):
        return self.hidden[x][y] == 1

    def reset(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                self.hidden[i][j] = 0
                self.visible[i][j] = 0
                self.mask[i][j] = 0
