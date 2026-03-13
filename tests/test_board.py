import pytest
from boardlib import Board
from boardlib.exceptions import OutOfBoundsError


@pytest.fixture
def board():
    return Board(15, 15)


# --- init --- #

def test_initial_board_is_empty(board):
    assert board.get(0, 0) == Board.EMPTY
    assert board.get(7, 7) == Board.EMPTY
    assert board.get(14, 14) == Board.EMPTY


def test_width_height(board):
    assert board.width == 15
    assert board.height == 15


# --- place --- #

def test_place(board):
    board.place(3, 4, 1)
    assert board.get(3, 4) == 1


def test_place_overwrite(board):
    board.place(3, 4, 1)
    board.place(3, 4, 2)
    assert board.get(3, 4) == 2


def test_place_out_of_bounds(board):
    with pytest.raises(OutOfBoundsError):
        board.place(99, 99, 1)


# --- remove --- #

def test_remove(board):
    board.place(3, 4, 1)
    board.remove(3, 4)
    assert board.get(3, 4) == Board.EMPTY


def test_remove_out_of_bounds(board):
    with pytest.raises(OutOfBoundsError):
        board.remove(99, 99)


# --- get / __getitem__ --- #

def test_get_and_getitem_same(board):
    board.place(3, 4, 1)
    assert board.get(3, 4) == board[3, 4]


def test_get_out_of_bounds(board):
    with pytest.raises(OutOfBoundsError):
        board.get(99, 99)


# --- is_valid --- #

def test_is_valid_inside(board):
    assert board.is_valid(0, 0) is True
    assert board.is_valid(14, 14) is True
    assert board.is_valid(7, 7) is True


def test_is_valid_outside(board):
    assert board.is_valid(-1, 0) is False
    assert board.is_valid(0, -1) is False
    assert board.is_valid(15, 0) is False
    assert board.is_valid(0, 15) is False


# --- is_empty --- #

def test_is_empty(board):
    assert board.is_empty(3, 4) is True
    board.place(3, 4, 1)
    assert board.is_empty(3, 4) is False


# --- is_full --- #

def test_is_full_false(board):
    assert board.is_full() is False


def test_is_full_true(board):
    board.fill(1)
    assert board.is_full() is True


# --- fill --- #

def test_fill(board):
    board.fill(1)
    assert board.get(0, 0) == 1
    assert board.get(7, 7) == 1
    assert board.get(14, 14) == 1


# --- reset --- #

def test_reset(board):
    board.fill(1)
    board.reset()
    assert board.get(0, 0) == Board.EMPTY
    assert board.get(7, 7) == Board.EMPTY
    assert board.get(14, 14) == Board.EMPTY


# --- copy --- #

def test_copy_same_values(board):
    board.place(3, 4, 1)
    copied = board.copy()
    assert copied.get(3, 4) == 1


def test_copy_is_independent(board):
    board.place(3, 4, 1)
    copied = board.copy()
    copied.place(3, 4, 2)
    assert board.get(3, 4) == 1


def test_copy_preserves_type():
    class SubBoard(Board):
        pass

    sub = SubBoard(15, 15)
    copied = sub.copy()
    assert type(copied) is SubBoard


# --- __str__ --- #

def test_str(board):
    board.place(0, 0, 1)
    result = str(board)
    lines = result.split("\n")
    assert len(lines) == 15
    assert lines[0].split()[0] == "1"
    assert lines[0].split()[1] == "0"