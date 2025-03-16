import enum

class Operators(enum.Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'

class Numberic:
    def __init__(self, denominator, numerator):
        self.denominator = denominator
        self.numerator = numerator

    def get_value(self):
        return self.numerator/self.denominator

class EquationNode:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    def add_left_child(self, child):
        self.left = child

    def add_right_child(self, child):
        self.right = child

    def traverse(self):
        if self.left:
            self.left.traverse()
        if self.right:
            self.right.traverse()

        if type(self.value) == Numberic:
            print(self.value.get_value())
        else:
            print(self.value)

    def match_operator(self, operator,value1, value2):
        match operator:
            case Operators.ADD:
                return value1 + value2
            case Operators.SUB:
                return value1 - value2
            case Operators.MUL:
                return value1 * value2
            case Operators.DIV:
                return value1 / value2

    def evaluate(self):
        if not self.left and not self.right:
            return self.value.get_value()
        elif self.left:
            value1 = self.left.evaluate()
            value2 = self.right.evaluate()
            return self.match_operator(self.value, value1, value2)