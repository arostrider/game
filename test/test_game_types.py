import pytest

from src.game_types import Drawable, Sprite, SpriteSheet, StaticGameObject, MovableGameObject
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
COORDINATES.extend([(i, j) for i in range(-1, 1) for j in range(-1, 1)])


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


SPRITE_SHEET_DIMENSIONS = [(128, 192), (192, 128), (192, 192)]


@pytest.mark.parametrize(("width", "height"), SPRITE_SHEET_DIMENSIONS)
@pytest.mark.parametrize(("columns", "rows"), [(4, 4)])
@pytest.mark.parametrize(("x", "y"), COORDINATES)
@pytest.mark.parametrize(("subsprite_column", "subsprite_row"), COORDINATES)
def test_sprite_sheet(width, height, columns, rows, x, y, subsprite_column, subsprite_row):
    image = MockImage(width=width, height=height)
    sprite_sheet = SpriteSheet(image=image, columns=4, rows=4)

    assert sprite_sheet.width == width / columns
    assert sprite_sheet.height == height / rows

    assert sprite_sheet.curr_subsprite() == pygame.Rect(sprite_sheet.curr_column * sprite_sheet.width,
                                                        sprite_sheet.curr_row * sprite_sheet.height,
                                                        sprite_sheet.width,
                                                        sprite_sheet.height)

    assert sprite_sheet.draw_kwargs(
        x, y, subsprite_column, subsprite_row) == {"source": sprite_sheet.image,
                                                   "dest": sprite_sheet.desired_on_screen_position(x, y),
                                                   "area": sprite_sheet.curr_subsprite()}


@pytest.mark.parametrize(("width", "height"), COORDINATES)
@pytest.mark.parametrize(("x", "y"), COORDINATES)
def test_static_game_object(x, y, width, height):
    image = MockImage(width=width, height=height)
    static_game_object = StaticGameObject(sprite=Sprite(image=image), start_position=(x, y))

    assert static_game_object.draw_sprite_kwargs() == static_game_object.sprite.draw_kwargs(x, y)


@pytest.mark.parametrize(("width", "height"), SPRITE_SHEET_DIMENSIONS)
@pytest.mark.parametrize(("x", "y"), [(-10, -10), (0, 0), (10, 10)])
@pytest.mark.parametrize(("curr_column", "curr_row"), [(i, j) for i in range(4) for j in range(4)])
def test_movable_game_object(x, y, width, height, curr_column, curr_row):
    image = MockImage(width=width, height=height)
    mgo = MovableGameObject(sprite=SpriteSheet(image=image, columns=4, rows=4), start_position=(x, y), start_speed=5)

    mgo.sprite.curr_column = curr_column
    mgo.sprite.curr_row = curr_row

    assert mgo.draw_sprite_kwargs() == mgo.sprite.draw_kwargs(mgo.x,
                                                              mgo.y,
                                                              column=mgo.sprite.curr_column,
                                                              row=mgo.sprite.curr_row)
