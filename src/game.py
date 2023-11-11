import pygame

from config import GameWindow, ContentDir
from game_types import Player, SpriteSheet, Sprite

if __name__ == "__main__":
    pygame.init()

    timer = pygame.time.Clock()
    window = pygame.display.set_mode((GameWindow.WIDTH, GameWindow.HEIGHT))

    pygame.display.set_caption(GameWindow.CAPTION)

    grass = Sprite(pygame.image.load(ContentDir.GRAPHICS / "grass.png"))

    player = Player(sprite=SpriteSheet(pygame.image.load(ContentDir.GRAPHICS / "girl.png"),
                                       columns=4,
                                       rows=4),
                    start_position=(20, 20),
                    start_speed=5)

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        window.fill(GameWindow.BACKGROUND_COLOR)
        window.blit(**grass.draw_kwargs(0, 0))

        player.handle_keys()
        window.blit(**player.draw_sprite_kwargs())

        pygame.display.update()
        timer.tick(GameWindow.FPS)
