import random
import enum
import equation as eq


class Operators(enum.Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'

class Brackets(enum.Enum):
    LEFT = '('
    RIGHT = ')'
    NULL = None

class Numberic:
    def __init__(self, denominator, numerator):
        self.denominator = denominator
        self.numerator = numerator

class Expression:
    def __init__(self, value, operator , bracket=Brackets.NULL):
        self.value = value
        self.operator = operator
        self.bracket = bracket



