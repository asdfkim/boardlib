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
        row, col = pos
        return self.get(row, col)

    def __setitem__(self, pos: tuple[int, int], stone: int) -> None:
        row, col = pos
        self.place(row, col, stone)

    def __str__(self) -> str:
        # Board의 책임에 사실 시각화는 없다고 생각함
        # 그래도 이정도는 그냥 넣어봄

        return "\n".join(
            " ".join(str(self._board[row, col]) for col in range(self._width))
            for row in range(self._height)
        )

    # --- #

    def is_valid(self, row: int, col: int) -> bool:
        return bool(0 <= row < self._height and 0 <= col < self._width)

    def is_empty(self, row: int, col: int) -> bool:
        self._validate(row, col)
        return bool(self._board[row, col] == self.EMPTY)

    def is_full(self) -> bool:
        return bool(np.all(self._board != self.EMPTY))

    # --- #

    def get(self, row: int, col: int) -> int:
        self._validate(row, col)
        return int(self._board[row, col])

    def place(self, row: int, col: int, stone: int) -> None:
        # 사실 '이미 돌이 있는 자리에 돌을 두어도 되는가?' 에 대한 검증 로직을 둘지 말지 고민했었음.
        # 결과적으로는 검증 로직을 제거하기로 결정함. = 'Board 의 책임에는 게임 관련 로직이 없어야 한다.' 라고 판단.

        self._validate(row, col)
        self._board[row, col] = stone

    def remove(self, row: int, col: int) -> None:
        self.place(row, col, self.EMPTY)

    def fill(self, stone: int) -> None:
        self._board[:] = stone

    def reset(self) -> None:
        self.fill(self.EMPTY)

    def copy(self) -> Self:
        return copy.deepcopy(self)

    # --- #

    def _validate(self, row: int, col: int) -> None:
        if not self.is_valid(row, col):
            raise OutOfBoundsError()