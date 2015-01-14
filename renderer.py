import pygame

black = (0, 0, 0)
red = (255, 0, 0)
red_hover = (150, 0, 0)
grey = (204, 204, 204)
white = (255, 255, 255, 125)


class GameRenderer:
    def __init__(self, screen):
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))

        self.font = pygame.font.Font(None, 36)

        self.timer_text = self.font.render("Timer: ", 1, black)
        self.easy_text = self.font.render("Easy", 1, black)
        self.medium_text = self.font.render("Medium", 1, black)
        self.hard_text = self.font.render("Hard", 1, black)
        self.retry_text = self.font.render("Retry", 1, black)

    def render(self, screen, game):
        self.background.fill((255, 255, 255))
        self.font = pygame.font.Font(None, 76)
        title1 = self.font.render("Memory", 1, black)
        self.background.blit(title1, (200, 15))
        title2 = self.font.render("Game", 1, red)
        self.background.blit(title2, (420, 15))

        # Draw board
        pygame.draw.rect(self.background, black,
                         (game.board_start_w, game.board_start_h, game.board_size, game.board_size), 4)

        # Draw board cells
        for i in range(game.board.SIZE):
            for j in range(game.board.SIZE):
                x = game.board_start_w + i * game.board.tile_size
                y = game.board_start_h + j * game.board.tile_size

                if game.board.visible[j][i]:
                    pygame.draw.rect(self.background,
                                     red,
                                     (x + 2, y + 2, game.board.tile_size - 2, game.board.tile_size - 2),
                                     0)

                if game.board.mask[j][i]:
                    color = red_hover if game.board.visible[j][i] else grey
                    pygame.draw.rect(self.background,
                                     color,
                                     (x + 2, y + 2, game.board.tile_size - 2, game.board.tile_size - 2),
                                     0)
                pygame.draw.rect(self.background,
                                 black,
                                 (x, y, game.board.tile_size, game.board.tile_size),
                                 2)

        # Timer
        self.font = pygame.font.Font(None, 36)
        seconds = 0 if (game.seconds - game.INPUT_TIME) < 0 else game.seconds - game.INPUT_TIME
        self.timer_text = self.font.render("Timer: " + str(seconds), 1, red)
        self.background.blit(self.timer_text, (game.menu_start_h, game.board_start_h))
        self.timer_text = self.font.render("Timer: ", 1, black)
        self.background.blit(self.timer_text, (game.menu_start_h, game.board_start_h))

        # Reset font size
        self.font = pygame.font.Font(None, 36)

        # Easy button
        color = red if game.should_hover_easy else black
        self.easy_text = self.font.render("Easy", 1, red if game.selected_difficulty == 0 else black)
        pygame.draw.rect(self.background,
                         red if game.selected_difficulty == 0 else color,
                         (game.menu_start_h, game.board_start_h + game.button_h + game.padding, game.button_w,
                          game.button_h),
                         2)
        self.background.blit(self.easy_text, (
            game.menu_start_h + game.button_w / 4 + 10, game.board_start_h + game.button_h + game.button_h / 4))

        # Medium button
        color = red if game.should_hover_medium else black
        self.medium_text = self.font.render("Medium", 1, red if game.selected_difficulty == 1 else black)
        pygame.draw.rect(self.background,
                         red if game.selected_difficulty == 1 else color,
                         (game.menu_start_h, game.board_start_h + game.button_h * 2 + game.padding * 2, game.button_w,
                          game.button_h),
                         2)
        self.background.blit(self.medium_text, (
            game.menu_start_h + game.button_w / 4 - 4, game.board_start_h + game.button_h * 2 + game.button_h / 4))

        # Hard button
        color = red if game.should_hover_hard else black
        self.hard_text = self.font.render("Hard", 1, red if game.selected_difficulty == 2 else black)
        pygame.draw.rect(self.background,
                         red if game.selected_difficulty == 2 else color,
                         (game.menu_start_h, game.board_start_h + game.button_h * 3 + game.padding * 3, game.button_w,
                          game.button_h),
                         2)
        self.background.blit(self.hard_text, (game.menu_start_h + game.button_w / 4 + 10,
                                              game.board_start_h + game.button_h * 3 + game.button_h / 4 + game.padding))

        # Play/Retry button
        color = red if game.should_hover_retry else black
        if game.first:
            self.retry_text = self.font.render("Play!", 1, red if game.should_hover_retry else black)
        else:
            self.retry_text = self.font.render("Retry", 1, red if game.should_hover_retry else black)
        pygame.draw.rect(self.background,
                         color,
                         (game.menu_start_h, game.board_start_h + game.board_size - game.button_h, game.button_w,
                          game.button_h),
                         2)
        self.background.blit(self.retry_text, (game.menu_start_h + game.button_w / 4 + 12,
                                               game.board_start_h + game.board_size - game.button_h + game.button_h / 4 - game.padding))

        # Handle 'Game Over' case
        if game.over:
            # Mark wrong cell with an 'X'
            (i, j) = game.bad_move
            x = game.board_start_w + j * game.board.tile_size
            y = game.board_start_h + i * game.board.tile_size
            pygame.draw.line(self.background, black, (x, y), (x + game.board.tile_size, y + game.board.tile_size), 3)
            pygame.draw.line(self.background, black, (x + game.board.tile_size, y), (x, y + game.board.tile_size), 3)

            self.show_hidden_board(game)

            overlay = pygame.Surface((game.board_size + 4, game.board_size + 4), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 128))  # notice the alpha value in the color
            self.font = pygame.font.Font(None, 80)

            over_text = self.font.render("Game over!", 1, black)
            overlay.blit(over_text, (game.board_start_w - 50, game.board_start_h + 30))

            self.background.blit(overlay, (game.board_start_w - 2, game.board_start_h - 2))

        # Handle 'Game Won' case
        if game.won:
            overlay = pygame.Surface((game.board_size + 4, game.board_size + 4), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 128))  # notice the alpha value in the color
            self.font = pygame.font.Font(None, 80)

            won_text = self.font.render("You won!", 1, black)
            overlay.blit(won_text, (game.board_start_w - 35, game.board_start_h + 30))

            self.background.blit(overlay, (game.board_start_w - 2, game.board_start_h - 2))

        screen.blit(self.background, (0, 0))

        pygame.display.flip()

    def show_hidden_board(self, game):
        for i in range(game.board.SIZE):
            for j in range(game.board.SIZE):
                x = game.board_start_w + i * game.board.tile_size
                y = game.board_start_h + j * game.board.tile_size

                if game.board.visible[j][i] == 0 and game.board.hidden[j][i] == 1:
                    pygame.draw.rect(self.background,
                                     red,
                                     (x + 6, y + 6, game.board.tile_size - 12, game.board.tile_size - 12),
                                     4)
