class BoardError(Exception): pass

class OutOfBoundsError(BoardError): pass

class OccupiedError(BoardError): pass