import abc
import logging

import pygame

from src.sprite_sheet_maps import GirlSubsprite


class Drawable(abc.ABC):
    def __init__(self, image: pygame.Surface):
        self.image = image

    @property
    @abc.abstractmethod
    def width(self) -> float:
        ...

    @property
    @abc.abstractmethod
    def height(self) -> float:
        ...

    def desired_on_screen_position(self, x: float, y: float) -> pygame.Rect:
        return pygame.Rect(x, y, self.width, self.height)

    @abc.abstractmethod
    def draw_kwargs(self, *args, **kwargs) -> dict:
        """Method preparing args to be used in pygame.Surface.blit method call"""
        ...


class Sprite(Drawable):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)

    @property
    def width(self) -> int:
        return self.image.get_width()

    @property
    def height(self) -> int:
        return self.image.get_height()

    def draw_kwargs(self, x: int, y: int) -> dict:
        return {"source": self.image,
                "dest": self.desired_on_screen_position(x, y)}


class SpriteSheet(Drawable):

    def __init__(self, image: pygame.Surface,
                 columns: int, rows: int,
                 start_column: int = 0, start_row: int = 0):
        super().__init__(image)
        self.columns = columns
        self.rows = rows

        # keeping tack of current subsprite position in the sheet
        self.curr_column = start_column
        self.curr_row = start_row

    @property
    def width(self) -> float:
        return self.image.get_width() / self.columns

    @property
    def height(self) -> float:
        return self.image.get_height() / self.rows

    def draw_kwargs(self, x: float, y: float, column: int, row: int) -> dict:
        """Method preparing kwargs to be used in pygame.Surface.blit method call"""
        return {"source": self.image,
                "dest": self.desired_on_screen_position(x, y),
                "area": pygame.Rect(
                    self.curr_column * self.width,
                    self.curr_row * self.height,
                    self.width,
                    self.height)}


class GameObject(abc.ABC):
    def __init__(self, sprite, start_position: tuple[float, float]):
        self.sprite = sprite
        self.x, self.y = start_position

    @abc.abstractmethod
    def draw_sprite_kwargs(self, *args, **kwargs) -> dict:
        ...


class StaticGameObject(GameObject):
    def __init__(self, sprite: Sprite, start_position: tuple[float, float]):
        super().__init__(sprite, start_position)

    def draw_sprite_kwargs(self) -> dict:
        return self.sprite.draw_kwargs(self.x, self.y)


class MovableGameObject(GameObject):
    def __init__(self, sprite: SpriteSheet, start_position: tuple[float, float], start_speed: float):
        super().__init__(sprite, start_position)
        self.speed = start_speed

    def draw_sprite_kwargs(self) -> dict:
        return self.sprite.draw_kwargs(self.x, self.y, column=self.sprite.curr_column, row=self.sprite.curr_row)

    def move(self, direction: tuple[int, int]):
        dir_x, dir_y = direction

        self.x = self.x + dir_x * self.speed
        self.y = self.y + dir_y * self.speed

        i = self.sprite.curr_column + 1 if self.sprite.curr_column != 3 else 0
        new_subsprite = None

        if dir_x == 1:
            new_subsprite = GirlSubsprite.RIGHT[i]
        elif dir_x == -1:
            new_subsprite = GirlSubsprite.LEFT[i]

        if dir_y == 1:
            new_subsprite = GirlSubsprite.DOWN[i]
        elif dir_y == -1:
            new_subsprite = GirlSubsprite.UP[i]

        self.sprite.curr_column, self.sprite.curr_row = new_subsprite

        logging.debug(f"Moving object to {self.x}, {self.y}\n"
                      f"New sprite phase / direction: {self.sprite.curr_column} / {self.sprite.curr_row}"
                      f"\n")


class Player(MovableGameObject):
    def __init__(self, sprite: SpriteSheet, start_position: tuple[float, float], start_speed: float):
        super().__init__(sprite, start_position, start_speed)

    def handle_keys(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_DOWN]:
            self.move((0, 1))
        elif key[pygame.K_UP]:
            self.move((0, -1))

        if key[pygame.K_RIGHT]:
            self.move((1, 0))
        elif key[pygame.K_LEFT]:
            self.move((-1, 0))

        if not any((key[pygame.K_DOWN], key[pygame.K_UP], key[pygame.K_RIGHT], key[pygame.K_LEFT])):
            # sprite stand still
            self.sprite.curr_column = GirlSubsprite.STANDING
