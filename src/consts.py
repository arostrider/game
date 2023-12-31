class GirlSubsprite:
    STANDING = 1  # index of subsprites which represent the girl standing pose

    DOWN = ((0, 0),
            (1, 0),
            (2, 0),
            (3, 0))
    UP = ((0, 1),
          (1, 1),
          (2, 1),
          (3, 1))
    LEFT = ((0, 2),
            (1, 2),
            (2, 2),
            (3, 2))
    RIGHT = ((0, 3),
             (1, 3),
             (2, 3),
             (3, 3))


class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
