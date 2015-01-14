import pygame

from board import Board


class GameEngine:
    difficulty = [
        {'GENERATE_TIME': 1,
         'HIDE_TIME': 3,
         'INPUT_TIME': 3},
        {'GENERATE_TIME': 1,
         'HIDE_TIME': 4,
         'INPUT_TIME': 4},
        {'GENERATE_TIME': 1,
         'HIDE_TIME': 5,
         'INPUT_TIME': 5}
    ]

    milliseconds = 0
    seconds = 0

    last_i = 0
    last_j = 0

    def __init__(self):
        self.board = Board(0)

        self.button_w = 158  # Button width
        self.button_h = 40   # Button height
        self.padding = 2     # Button padding

        self.board_start_w = 104  # X coordinate of board's top left corner
        self.board_start_h = 108  # Y coordinate of board's top left corner
        self.board_size = 384     # Board width and height
        self.menu_start_h = self.board_start_w + self.board_size + 50  # X coordinate of menu's top left corner

        self.selected_difficulty = 0
        self.GENERATE_TIME = 2
        self.HIDE_TIME = 4
        self.INPUT_TIME = 4

        self.first = True
        self.over = False
        self.won = False

        self.generated = False
        self.hidden = False

        self.should_hover_easy = False
        self.should_hover_medium = False
        self.should_hover_hard = False
        self.should_hover_retry = False

        self.bad_move = (-1, -1)

    def start(self, selected):
        self.first = False
        self.board = Board(selected)  # Get new board of the selected difficulty
        self.GENERATE_TIME = self.difficulty[selected]['GENERATE_TIME']
        self.HIDE_TIME = self.difficulty[selected]['HIDE_TIME']
        self.INPUT_TIME = self.difficulty[selected]['INPUT_TIME']

    def reset(self):
        self.over = False
        self.won = False
        self.milliseconds = self.seconds = 0
        self.generated = self.hidden = False
        self.last_i = self.last_j = 0
        self.bad_move = (-1, -1)

    def won_game(self):
        for i in range(self.board.SIZE):
            for j in range(self.board.SIZE):
                if self.board.hidden[i][j] != self.board.visible[i][j]:
                    return False
        return True

    def mouse_over_easy(self):
        (x, y) = pygame.mouse.get_pos()
        x1 = self.menu_start_h
        x2 = x1 + self.button_w
        y1 = self.board_start_h + self.button_h + self.padding
        y2 = y1 + self.button_h
        return x1 <= x <= x2 and y1 <= y <= y2

    def clicked_easy(self):
        return self.mouse_over_easy() and 1 in pygame.mouse.get_pressed()

    def mouse_over_medium(self):
        (x, y) = pygame.mouse.get_pos()
        x1 = self.menu_start_h
        x2 = x1 + self.button_w
        y1 = self.board_start_h + self.button_h * 2 + self.padding * 2
        y2 = y1 + self.button_h
        return x1 <= x <= x2 and y1 <= y <= y2

    def clicked_medium(self):
        return self.mouse_over_medium() and 1 in pygame.mouse.get_pressed()

    def mouse_over_hard(self):
        (x, y) = pygame.mouse.get_pos()
        x1 = self.menu_start_h
        x2 = x1 + self.button_w
        y1 = self.board_start_h + self.button_h * 3 + self.padding * 3
        y2 = y1 + self.button_h
        return x1 <= x <= x2 and y1 <= y <= y2

    def clicked_hard(self):
        return self.mouse_over_hard() and 1 in pygame.mouse.get_pressed()

    def mouse_over_retry(self):
        (x, y) = pygame.mouse.get_pos()
        x1 = self.menu_start_h
        x2 = x1 + self.button_w
        y1 = self.board_start_h + self.board_size - self.button_h
        y2 = y1 + self.button_h
        return x1 <= x <= x2 and y1 <= y <= y2

    def clicked_retry(self):
        return self.mouse_over_retry() and 1 in pygame.mouse.get_pressed()

    def in_bounds(self, i, j):
        return i in range(self.board.SIZE) and j in range(self.board.SIZE)

    def get_board_indices(self, x, y):
        x -= self.board_start_w
        y -= self.board_start_h

        x = int(x / self.board.tile_size)
        y = int(y / self.board.tile_size)

        return x, y

    def clicked_board(self):
        if 1 in pygame.mouse.get_pressed():
            (x, y) = pygame.mouse.get_pos()
            (i, j) = self.get_board_indices(x, y)
            return self.in_bounds(j, i)

    def handle_buttons_hover(self):
        self.should_hover_easy = self.should_hover_medium = self.should_hover_hard = self.should_hover_retry = False
        if self.mouse_over_easy():
            self.should_hover_easy = True
        elif self.mouse_over_medium():
            self.should_hover_medium = True
        elif self.mouse_over_hard():
            self.should_hover_hard = True
        elif self.mouse_over_retry():
            self.should_hover_retry = True

    def update_hover_mask(self):
        if self.over or self.won:
            return

        (x, y) = pygame.mouse.get_pos()
        (i, j) = self.get_board_indices(x, y)

        if not self.in_bounds(i, j):
            self.board.mask[self.last_j][self.last_i] = 0
            self.last_i = 0
            self.last_j = 0
            return

        if i != self.last_i or j != self.last_j:
            self.board.mask[self.last_j][self.last_i] = 0
            self.board.mask[j][i] = 1
            self.last_i = i
            self.last_j = j

    def handle_input(self):
        # Check if buttons were clicked
        if self.clicked_easy():
            self.selected_difficulty = 0
        elif self.clicked_medium():
            self.selected_difficulty = 1
        elif self.clicked_hard():
            self.selected_difficulty = 2
        elif self.clicked_retry():
            self.board.reset()
            self.reset()
            self.start(self.selected_difficulty)
            return

        # Check if board was clicked
        if self.clicked_board():
            (x, y) = pygame.mouse.get_pos()
            (i, j) = self.get_board_indices(x, y)

            # Mark cell as hit
            if not self.over and not self.won:
                self.board.visible[j][i] = 1

            # Check if bad move
            if not self.won and not self.board.is_correct_move(j, i):
                self.bad_move = (j, i)
                self.over = True
                return

            # Check if game won
            if self.won_game():
                self.won = True
                return

        # Handle buttons hover
        self.handle_buttons_hover()

        # Update board's hover mask
        self.update_hover_mask()

    def handle_menu_input(self):
        # Check if buttons were clicked
        if self.clicked_easy():
            self.selected_difficulty = 0
            self.board.reset()
            self.reset()
            self.start(self.selected_difficulty)
        elif self.clicked_medium():
            self.selected_difficulty = 1
            self.board.reset()
            self.reset()
            self.start(self.selected_difficulty)
        elif self.clicked_hard():
            self.selected_difficulty = 2
            self.board.reset()
            self.reset()
            self.start(self.selected_difficulty)
        elif self.clicked_retry():
            self.board.reset()
            self.reset()
            self.start(self.selected_difficulty)
            return

        # Handle buttons hover
        self.handle_buttons_hover()

    def update(self, delta):
        """ Does nothing until 'Play/Retry' was pressed """

        if self.first:
            self.handle_menu_input()
            if self.clicked_retry():
                self.first = False
            return

        # Update seconds
        self.milliseconds += delta
        if self.milliseconds > 1000:
            if not self.over and not self.won:
                self.seconds += 1
            self.milliseconds = 0

        # Generate board
        if self.seconds == self.GENERATE_TIME and not self.generated:
            self.board.generate()
            for i in range(self.board.SIZE):
                self.board.visible[i] = list(self.board.hidden[i])
            self.generated = True

        # Hide board
        if self.seconds == self.HIDE_TIME and not self.hidden:
            # Hide board
            self.board.clear_visible()
            self.hidden = True

        # Handle user input
        if self.seconds >= self.INPUT_TIME:
            self.handle_input()
