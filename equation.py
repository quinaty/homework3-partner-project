import enum

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

    def get_value(self):
        return self.numerator/self.denominator

class Expression:
    def __init__(self, value, operator , bracket=Brackets.NULL):
        self.value = value
        self.operator = operator
        self.bracket = bracket

class EquationTree:
    def __init__(self, expn, left, right, parent=None):
        self.expn = expn
        self.left = left
        self.right = right
        self.parent = parent

    def add_left_child(self, child):
        self.left = child

    def add_right_child(self, child):
        self.right = child


    def traverse(self):
        print(str(self.expn.value.denominator/self.expn.value.numerator),str(self.expn.operator),str(self.expn.bracket))
        if self.left is not None:
            self.left.traverse()
        if self.right is not None:
            self.right.traverse()


    def evaluate(self):
        value = 0
        operator = Operators.ADD
        is_get_value = False
        if self.left is not None:
            value = self.left.evaluate()
            operator = self.left.expn.operator
            is_get_value = True
        if self.right is not None:
            value = self.right.evaluate()
            operator = self.right.expn.operator
            is_get_value = True

        match operator:
            case Operators.ADD:
                return  self.expn.value.get_value() + value
            case Operators.SUB:
                return  self.expn.value.get_value() - value
            case Operators.MUL:
                if not is_get_value:
                    value = 1
                return  self.expn.value.get_value() * value
            case Operators.DIV:
                if not is_get_value:
                    value = 1
                return  self.expn.value.get_value() / value