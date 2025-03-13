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

def generate_equation(r):
    root = eq.EquationTree(generate_expression(generate_numberic(r)),None,None)
    current = root
    parent = None
    for i in range(4):
        node = eq.EquationTree(generate_expression(generate_numberic(r)),None,None)
        if node.expn.operator == Operators.ADD or node.expn.operator == Operators.SUB or (parent.expn.bracket and parent.expn.bracket == Brackets.RIGHT):
            current.add_right_child(node)
        else :
            if node.expn.operator == Operators.MUL or node.expn.operator == Operators.DIV or (node.expn.bracket and node.expn.bracket == Brackets.LEFT):
                current.add_left_child(node)

        if i == 1:
            parent = root
        else:
         parent = current

        current = node

    return root


if __name__ == '__main__':
    r = 10
    root = generate_equation(r)
    root.traverse()
