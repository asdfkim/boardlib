class BoardError(Exception): pass

class OutOfBoundsError(BoardError, IndexError): pass