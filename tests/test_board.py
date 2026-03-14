import pytest
from boardlib import Board
from boardlib.exceptions import OutOfBoundsError


@pytest.fixture
def board():
    return Board(15, 15, default=0)


# --- __init__ --- #

def test_initial_board_has_default_value(board):
    assert board[0, 0]   == 0
    assert board[7, 7]   == 0
    assert board[14, 14] == 0


def test_width_height(board):
    assert board.width  == 15
    assert board.height == 15


def test_default_value(board):
    assert board.default == 0


def test_invalid_size_raises():
    with pytest.raises(ValueError):
        Board(0, 5, default=0)

    with pytest.raises(ValueError):
        Board(5, 0, default=0)

    with pytest.raises(ValueError):
        Board(-1, -1, default=0)


# --- __setitem__ / __getitem__ --- #

def test_setitem_and_getitem(board):
    board[3, 4] = 1
    assert board[3, 4] == 1


def test_setitem_overwrite(board):
    board[3, 4] = 1
    board[3, 4] = 2
    assert board[3, 4] == 2


def test_setitem_out_of_bounds(board):
    with pytest.raises(OutOfBoundsError):
        board[99, 99] = 1


def test_getitem_out_of_bounds(board):
    with pytest.raises(OutOfBoundsError):
        _ = board[99, 99]


def test_getitem_returns_reference(board):
    inner = [1, 2, 3]
    b = Board(3, 3, default=None)
    b[0, 0] = inner
    b[0, 0].append(4)
    assert inner == [1, 2, 3, 4]


# --- __eq__ --- #

def test_eq_same_boards():
    b1 = Board(3, 3, default=0)
    b2 = Board(3, 3, default=0)
    assert b1 == b2


def test_eq_different_values():
    b1 = Board(3, 3, default=0)
    b2 = Board(3, 3, default=0)
    b1[0, 0] = 1
    assert b1 != b2


def test_eq_different_size():
    assert Board(3, 3, default=0) != Board(4, 4, default=0)


def test_eq_different_default():
    assert Board(3, 3, default=0) != Board(3, 3, default=None)


# --- __repr__ --- #

def test_repr(board):
    assert repr(board) == "Board(width=15, height=15, default=0)"


# --- __str__ --- #

def test_str_shape(board):
    lines = str(board).split("\n")
    assert len(lines) == 15
    assert all(len(line.split()) == 15 for line in lines)


def test_str_reflects_setitem(board):
    board[0, 0] = 9
    lines = str(board).split("\n")
    assert lines[0].split()[0] == "9"
    assert lines[0].split()[1] == "0"


# --- is_valid --- #

def test_is_valid_inside(board):
    assert board.is_valid(0,  0)  is True
    assert board.is_valid(14, 14) is True
    assert board.is_valid(7,  7)  is True


def test_is_valid_outside(board):
    assert board.is_valid(-1, 0)  is False
    assert board.is_valid(0,  -1) is False
    assert board.is_valid(15, 0)  is False
    assert board.is_valid(0,  15) is False


# --- fill --- #

def test_fill(board):
    board.fill(7)
    assert board[0,  0]  == 7
    assert board[7,  7]  == 7
    assert board[14, 14] == 7


def test_fill_shares_reference():
    shared = []
    b = Board(2, 2, default=None)
    b.fill(shared)
    b[0, 0].append(1)
    assert b[1, 1] == [1] # 같은 참조


# --- reset --- #

def test_reset(board):
    board.fill(7)
    board.reset()
    assert board[0,  0]  == 0
    assert board[7,  7]  == 0
    assert board[14, 14] == 0


# --- copy --- #

def test_copy_same_values(board):
    board[3, 4] = 1
    copied = board.copy()
    assert copied[3, 4] == 1


def test_copy_is_independent(board):
    board[3, 4] = 1
    copied = board.copy()
    copied[3, 4] = 2
    assert board[3, 4] == 1


def test_copy_preserves_subclass():
    class SubBoard(Board):
        pass

    sub = SubBoard(15, 15, default=0)
    assert type(sub.copy()) is SubBoard