import pytest
from boardlib import Board, Stone
from boardlib.exceptions import OutOfBoundsError


@pytest.fixture
def board():
    return Board(15, 15)


# --- 초기화 --- #

def test_initial_board_is_empty(board):
    assert board.get(0, 0) == Stone.EMPTY
    assert board.get(7, 7) == Stone.EMPTY
    assert board.get(14, 14) == Stone.EMPTY


def test_width_height(board):
    assert board.width == 15
    assert board.height == 15


# --- place --- #

def test_place(board):
    board.place(3, 4, Stone.BLACK)
    assert board.get(3, 4) == Stone.BLACK


def test_place_overwrite(board):
    board.place(3, 4, Stone.BLACK)
    board.place(3, 4, Stone.WHITE)
    assert board.get(3, 4) == Stone.WHITE


def test_place_out_of_bounds(board):
    with pytest.raises(OutOfBoundsError):
        board.place(99, 99, Stone.BLACK)


# --- remove --- #

def test_remove(board):
    board.place(3, 4, Stone.BLACK)
    board.remove(3, 4)
    assert board.get(3, 4) == Stone.EMPTY


def test_remove_out_of_bounds(board):
    with pytest.raises(OutOfBoundsError):
        board.remove(99, 99)


# --- get / __getitem__ --- #

def test_get_and_getitem_same(board):
    board.place(3, 4, Stone.BLACK)
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
    board.place(3, 4, Stone.BLACK)
    assert board.is_empty(3, 4) is False


# --- is_full --- #

def test_is_full_false(board):
    assert board.is_full() is False


def test_is_full_true(board):
    board.fill(Stone.BLACK)
    assert board.is_full() is True


# --- fill --- #

def test_fill(board):
    board.fill(Stone.BLACK)
    assert board.get(0, 0) == Stone.BLACK
    assert board.get(7, 7) == Stone.BLACK
    assert board.get(14, 14) == Stone.BLACK


# --- reset --- #

def test_reset(board):
    board.fill(Stone.BLACK)
    board.reset()
    assert board.get(0, 0) == Stone.EMPTY
    assert board.get(7, 7) == Stone.EMPTY
    assert board.get(14, 14) == Stone.EMPTY


# --- copy --- #

def test_copy_same_values(board):
    board.place(3, 4, Stone.BLACK)
    copied = board.copy()
    assert copied.get(3, 4) == Stone.BLACK


def test_copy_is_independent(board):
    board.place(3, 4, Stone.BLACK)
    copied = board.copy()
    copied.place(3, 4, Stone.WHITE)
    assert board.get(3, 4) == Stone.BLACK


def test_copy_preserves_type():
    class SubBoard(Board):
        pass

    sub = SubBoard(15, 15)
    copied = sub.copy()
    assert type(copied) is SubBoard