import abc

import pygame


class Drawable(abc.ABC):
    def __init__(self, image: pygame.Surface):
        self.image = image

    @property
    @abc.abstractmethod
    def width(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def height(self) -> int:
        ...

    def desired_on_screen_position(self, x: float, y: float) -> pygame.Rect:
        return pygame.Rect(x, y, self.width, self.height)

    @abc.abstractmethod
    def draw_kwargs(self, *args, **kwargs) -> dict:
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

    def draw_kwargs(self, x: int, y: int):
        """Method preparing args to be used in pygame.Surface.blit method call"""
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

    def draw_sprite_kwargs(self, column: int, row: int) -> dict:
        return self.sprite.draw_kwargs(self.x, self.y, column, row)


class MovableGameObject(GameObject):
    def __init__(self, sprite: Drawable, start_position: tuple[float, float], start_speed: float):
        super().__init__(sprite, start_position)
        self.speed = start_speed

    def move(self, direction: tuple[int, int]):
        self.x = self.x + direction[0] * self.speed
        self.y = self.y + direction[1] * self.speed

        # TODO: replace with debugger
        print(self.x)
        print(self.y)
        print()


class Player(MovableGameObject):
    def __init__(self, sprite: Drawable, start_position: tuple[float, float], start_speed: float):
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
