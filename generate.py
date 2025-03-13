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


def generate_numberic(r):
    denominator = random.randint(0, r)
    numerator = random.randint(1, r)
    numberic = Numberic(denominator, numerator)
    return numberic

def generate_expression(value):
    operator = random.choice(list(Operators))
    bracket = random.choice(list(Brackets))
    exp = Expression(value, operator, bracket)
    return exp




if __name__ == '__main__':
    r = 10
