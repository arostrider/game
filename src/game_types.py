import abc

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

    def __init__(self, image: pygame.Surface, columns: int, rows: int):
        super().__init__(image)
        self.columns = columns
        self.rows = rows

    @property
    def width(self) -> float:
        return self.image.get_width() / self.columns

    @property
    def height(self) -> float:
        return self.image.get_height() / self.rows

    def subsprite(self, column: int, row: int) -> pygame.Rect:
        return pygame.Rect(
            column * self.width,
            row * self.height,
            self.width,
            self.height)

    def draw_kwargs(self, x: float, y: float, column: int, row: int) -> dict:
        """Method preparing kwargs to be used in pygame.Surface.blit method call"""
        return {"source": self.image,
                "dest": self.desired_on_screen_position(x, y),
                "area": self.subsprite(column, row)}


class GameObject(abc.ABC):
    def __init__(self, sprite: Drawable, start_position: tuple[float, float]):
        self.sprite = sprite
        self.x, self.y = start_position

    @abc.abstractmethod
    def draw_sprite_kwargs(self, *args, **kwargs) -> dict:
        ...


class MovableGameObject(GameObject):
    def __init__(self, sprite: Drawable, start_position: tuple[float, float], start_speed: float):
        super().__init__(sprite, start_position)
        self.speed = start_speed

        self.sprite_phase = 0
        self.sprite_direction = 0

    def draw_sprite_kwargs(self) -> dict:
        return self.sprite.draw_kwargs(self.x, self.y, row=self.sprite_direction, column=self.sprite_phase)

    def move(self, direction: tuple[int, int]):
        dir_x, dir_y = direction

        self.x = self.x + dir_x * self.speed
        self.y = self.y + dir_y * self.speed

        i = self.sprite_phase + 1 if self.sprite_phase != 3 else 0
        new_subsprite = None

        if dir_x == 1:
            new_subsprite = GirlSubsprite.RIGHT[i]
        elif dir_x == -1:
            new_subsprite = GirlSubsprite.LEFT[i]

        if dir_y == 1:
            new_subsprite = GirlSubsprite.DOWN[i]
        elif dir_y == -1:
            new_subsprite = GirlSubsprite.UP[i]

        self.sprite_phase, self.sprite_direction = new_subsprite

        # TODO: replace with debugger
        print(f"Moving object to {self.x}, {self.y}\n"
              f"New sprite phase / direction: {self.sprite_phase} / {self.sprite_direction}"
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
