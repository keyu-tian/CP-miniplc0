from collections import namedtuple
from enum import Enum, auto


class TokenType(Enum):
    NULL_TOKEN = auto()
    UNSIGNED_INTEGER = auto()
    IDENTIFIER = auto()
    
    BEGIN = auto()
    END = auto()
    VAR = auto()
    CONST = auto()
    PRINT = auto()
    
    PLUS_SIGN = auto()
    MINUS_SIGN = auto()
    MULTIPLICATION_SIGN = auto()
    DIVISION_SIGN = auto()
    EQUAL_SIGN = auto()
    SEMICOLON = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()


Token = namedtuple('Token', ['token_type', 'val'])


STR_TO_TOKEN_TYPE = {
    'begin': TokenType.BEGIN, 'end': TokenType.END,
    'const': TokenType.CONST, 'var': TokenType.VAR, 'print': TokenType.PRINT,
    '+': TokenType.PLUS_SIGN,
    '-': TokenType.MINUS_SIGN,
    '*': TokenType.MULTIPLICATION_SIGN,
    '/': TokenType.DIVISION_SIGN,
    '=': TokenType.EQUAL_SIGN,
    ';': TokenType.SEMICOLON,
    '(': TokenType.LEFT_BRACKET,
    ')': TokenType.RIGHT_BRACKET,
}
