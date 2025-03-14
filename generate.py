import random
import enum
import equation as eq

class Brackets_Stack:
    def __init__(self):
        self.stack = []

    def push(self, bracket):
        self.stack.append(bracket)

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0

    def length(self):
        return len(self.stack)


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

def generate_expression(value,is_root=False):
    rootlist = [Brackets.LEFT,Brackets.NULL]
    operator = Operators.ADD
    bracket = random.choice(rootlist)

    if not is_root:
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


def bracket_check(node, stack, remain_num):
    if node.expn.bracket == Brackets.RIGHT and stack.is_empty():
       return False
    if node.expn.bracket == Brackets.LEFT and remain_num == 1:
        return False

   # print(stack.length(), remain_num)

    required_num = stack.length()
    probability = random.random()
    if probability < required_num/remain_num:
        node.expn.bracket = Brackets.RIGHT

    return True


def generate_equation_tree(r,limit = 4):
    root = eq.EquationTree(generate_expression(generate_numberic(r), True),None,None)
    current = root
    expression_count = 1
    stack = Brackets_Stack()
    if root.expn.bracket == Brackets.LEFT:
        stack.push('(')

    while expression_count < limit :

        node = generate_expression_node(r, current, current.parent)

        if bracket_check(node, stack, limit - expression_count):
            if node.expn.bracket == Brackets.LEFT:
                stack.push('(')
            if node.expn.bracket == Brackets.RIGHT and not stack.is_empty():
                stack.pop()

            if expression_count == 0:
                current.parent = root
            else:
                node.parent = current

            current = node
            expression_count += 1

        else:
            current.left = None
            current.right = None
            continue

    return root


if __name__ == '__main__':
    r = 10
    equation = generate_equation_tree(r)
    equation.traverse()
