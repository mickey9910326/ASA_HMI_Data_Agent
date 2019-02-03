import enum

class AdtCmd(enum.IntEnum):
    TERM = 1
    LOADER = 2
    STK500 = 3

class AdtSubCmdLoader(enum.IntEnum):
    START = 1
    STATE = 2

class AdtSubCmdTerm(enum.IntEnum):
    OPEN  = 1
    CLOSE = 2
    CLEAR = 3
