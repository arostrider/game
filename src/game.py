import pygame

from src.config import GameWindow, ContentDir
from src.game_types import Player, SpriteSheet, Sprite, StaticGameObject

if __name__ == "__main__":
    pygame.init()

    timer = pygame.time.Clock()
    window = pygame.display.set_mode((GameWindow.WIDTH, GameWindow.HEIGHT))

    pygame.display.set_caption(GameWindow.CAPTION)

    grass_image = pygame.image.load(ContentDir.GRAPHICS / "grass.png")

    grasses = [StaticGameObject(sprite=Sprite(grass_image),
                                start_position=(x, y))
               for x in range(0, window.get_width(), grass_image.get_width())
               for y in range(0, window.get_height(), grass_image.get_height())]

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
        for grass in grasses:
            window.blit(**grass.draw_sprite_kwargs())

        player.handle_keys()
        window.blit(**player.draw_sprite_kwargs())

        pygame.display.update()
        timer.tick(GameWindow.FPS)
