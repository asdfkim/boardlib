import copy
from typing import Self

import numpy as np
from numpy.typing import NDArray

from .exceptions import OutOfBoundsError

class Board:
    EMPTY: int = 0

    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._board: NDArray[np.int_] = np.zeros((height, width), dtype=np.int_)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    # --- #

    def __getitem__(self, pos: tuple[int, int]) -> int:
        x, y = pos
        return self.get(x, y)

    def __setitem__(self, pos: tuple[int, int], value: int) -> None:
        x, y = pos
        self.place(x, y, value)

    def __str__(self) -> str:
        return "\n".join(
            " ".join(str(self._board[y, x]) for x in range(self._width))
            for y in range(self._height)
        )

    # --- #

    def is_valid(self, x: int, y: int) -> bool:
        return bool(0 <= x < self._width and 0 <= y < self._height)

    def is_empty(self, x: int, y: int) -> bool:
        self._validate(x, y)
        return bool(self._board[y, x] == self.EMPTY)

    def is_full(self) -> bool:
        return bool(np.all(self._board != self.EMPTY))

    # --- #

    def get(self, x: int, y: int) -> int:
        self._validate(x, y)
        return int(self._board[y, x])

    def place(self, x: int, y: int, value: int) -> None:
        self._validate(x, y)
        self._board[y, x] = value

    def remove(self, x: int, y: int) -> None:
        self.place(x, y, self.EMPTY)

    def fill(self, value: int) -> None:
        self._board[:] = value

    def reset(self) -> None:
        self.fill(self.EMPTY)

    def copy(self) -> Self:
        return copy.deepcopy(self)

    # --- #

    def _validate(self, x: int, y: int) -> None:
        if not self.is_valid(x, y):
            raise OutOfBoundsError()