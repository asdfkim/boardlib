import copy
from typing import (
    Self, Generic, TypeVar
)

from .exceptions import OutOfBoundsError

T = TypeVar('T')

class Board(Generic[T]):

    def __init__(self, width: int, height: int, default: T) -> None:
        if width <= 0 or height <= 0:
            raise ValueError(f"width and height must be positive, got ({width}, {height})")

        self._width   = width
        self._height  = height
        self._default = default

        self._board: list[list[T]] = [
            [default for _ in range(width)]
            for _ in range(height)
        ]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def default(self) -> T:
        """default 의 참조 반환"""
        return self._default

    # --- #

    def __getitem__(self, pos: tuple[int, int]) -> T:
        """복제본이 아닌 참조 반환"""
        x, y = pos
        self._validate(x, y)
        return self._board[y][x]

    def __setitem__(self, pos: tuple[int, int], value: T) -> None:
        """복제본이 아닌 참조로 저장"""
        x, y = pos
        self._validate(x, y)
        self._board[y][x] = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(width={self._width}, height={self._height}, default={self._default})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return (
                    self._width == other._width
                and self._height == other._height
                and self._default == other._default
                and self._board == other._board
        )

    def __str__(self) -> str:
        return "\n".join(
            " ".join(str(self._board[y][x]) for x in range(self._width))
            for y in range(self._height)
        )

    # --- #

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self._width and 0 <= y < self._height

    # [is_empty, is_full]
    # EMPTY 의 개념을 Board 에서 분리하였는데,
    # 이렇게 되면 공간이 비어있는지, 꽉 차있는지 모른다.
    # 따라서 제거하였다.

    # --- #

    def fill(self, value: T) -> None:
        """모든 공간을 value 의 참조로 채움"""
        self._board = [
            [value for _ in range(self._width)]
            for _ in range(self._height)
        ]

    def reset(self) -> None:
        self.fill(self._default)

    def copy(self) -> Self:
        return copy.deepcopy(self)

    # --- #

    def _validate(self, x: int, y: int) -> None:
        if not self.is_valid(x, y):
            raise OutOfBoundsError(f"({x}, {y}) is out of bounds for {self._width}x{self._height} board")