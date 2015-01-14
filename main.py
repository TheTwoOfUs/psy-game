import pygame

from pygame.constants import QUIT

from game import GameEngine
from renderer import GameRenderer


def main():
    pygame.init()
    pygame.display.set_caption("Memory game")
    screen = pygame.display.set_mode((800, 600))

    fps = 60

    game_engine = GameEngine()
    game_renderer = GameRenderer(screen)

    clock = pygame.time.Clock()

    while 1:
        delta = clock.tick(fps)

        game_engine.update(delta)
        game_renderer.render(screen, game_engine)

        for event in pygame.event.get():
            if event.type == QUIT:
                return


if __name__ == "__main__":
    main()
