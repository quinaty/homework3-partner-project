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

def generate_expression_node(r, current, parent):
    node = eq.EquationTree(generate_expression(generate_numberic(r)), None, None)

    if node.expn.operator == Operators.ADD or node.expn.operator == Operators.SUB or (
            parent and parent.expn.bracket == Brackets.RIGHT):
        current.add_right_child(node)
    else:
        if node.expn.operator == Operators.MUL or node.expn.operator == Operators.DIV or (
                node and node.expn.bracket == Brackets.LEFT):
            current.add_left_child(node)

    return node

def generate_equation_tree(r,limit = 4):
    root = eq.EquationTree(generate_expression(generate_numberic(r)),None,None)
    current = root
    bracket_count = 0
    expression_count = 1

    while True:
        if(expression_count == limit and bracket_count != 0):
            expression_count -= 1
            current = current.parent
            current.left = None
            current.right = None
        else:
            if expression_count == limit and bracket_count == 0:
                break

        node = generate_expression_node(r, current, current.parent)

        if node.expn.bracket == Brackets.LEFT:
            bracket_count += 1
        if node.expn.bracket == Brackets.RIGHT:
            bracket_count -= 1

        if expression_count == 1:
            current.parent = root
        else:
         node.parent = current

        current = node
        expression_count += 1

    return root


if __name__ == '__main__':
    r = 10
    root = generate_equation_tree(r)
    root.traverse()
