from boardlib import Stone

def test_stone_values():
    assert Stone.EMPTY ==  0
    assert Stone.BLACK ==  1
    assert Stone.WHITE == -1

def test_stone_is_int():
    assert isinstance(Stone.BLACK, int)
    assert isinstance(Stone.WHITE, int)
    assert isinstance(Stone.EMPTY, int)

def test_stone_int_comparison():
    assert Stone.BLACK ==  1
    assert Stone.WHITE == -1
    assert Stone.EMPTY ==  0

def test_stone_from_int():
    assert Stone(0)  == Stone.EMPTY
    assert Stone(1)  == Stone.BLACK
    assert Stone(-1) == Stone.WHITE