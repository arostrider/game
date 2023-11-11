from pathlib import Path

import pygame

from game_types import Player, SpriteSheet, Sprite

SCREEN_CAPTION = "Testing out Pygame!"
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 30
BACKGROUND_COLOR = pygame.Color(50, 200, 255)
GRAPHICS_DIR = Path("content/graphics")

if __name__ == "__main__":
    pygame.init()

    timer = pygame.time.Clock()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption(SCREEN_CAPTION)

    grass = Sprite(pygame.image.load(GRAPHICS_DIR / "grass.png"))

    player = Player(sprite=SpriteSheet(pygame.image.load(GRAPHICS_DIR / "girl.png"),
                                       columns=4,
                                       rows=4),
                    start_position=(20, 20),
                    start_speed=10)

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        window.fill(BACKGROUND_COLOR)

        player.handle_keys()
        window.blit(**player.draw_sprite_kwargs(column=0, row=0))

        pygame.display.update()
        timer.tick(FPS)
