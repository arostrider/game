import pytest

from src.game_types import Drawable, Sprite
import pygame


class DrawableChild(Drawable):
    def __init__(self, image, width: int, height: int):
        super().__init__(image)
        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def draw_kwargs(self) -> dict:
        raise NotImplemented


COORDINATES = [(i, j) for i in range(-64, 64, 32) for j in range(-64, 64, 32)]
COORDINATES.extend([(i, j) for i in range(-4, 4) for j in range(-4, 4)])


@pytest.mark.parametrize(("width", "height"), COORDINATES)
@pytest.mark.parametrize(("x", "y"), COORDINATES)
def test_drawable(width, height, x, y):
    drawable = DrawableChild(image="placeholder", width=width, height=height)

    assert drawable.image == "placeholder"
    assert drawable.desired_on_screen_position(x, y) == pygame.Rect(x, y, drawable.width, drawable.height)


class MockImage:
    def __init__(self, width: int, height: int):
        super().__init__()
        self._width = width
        self._height = height

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height


@pytest.mark.parametrize(("width", "height"), COORDINATES)
@pytest.mark.parametrize(("x", "y"), COORDINATES)
def test_sprite(width, height, x, y):
    image = MockImage(width=width, height=height)
    sprite = Sprite(image=image)

    assert sprite.width == width
    assert sprite.height == height

    assert sprite.draw_kwargs(x, y) == {"source": image,
                                        "dest": sprite.desired_on_screen_position(x, y)}
