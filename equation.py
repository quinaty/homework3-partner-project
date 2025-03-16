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

