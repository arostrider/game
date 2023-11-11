import pytest

from src.game_types import Drawable
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


COORDINATES = [(i, j) for i in range(-128, 128, 32) for j in range(-128, 128, 32)]


@pytest.mark.parametrize(("width", "height"), COORDINATES)
@pytest.mark.parametrize(("x", "y"), COORDINATES)
def test_drawable(width, height, x, y):
    drawable = DrawableChild(image="placeholder", width=width, height=height)

    assert drawable.desired_on_screen_position(x, y) == pygame.Rect(x, y, drawable.width, drawable.height)
