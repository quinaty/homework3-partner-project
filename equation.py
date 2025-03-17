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
        self.order = 0

        if type(value) == Numberic:
            self.order = value.get_value()
        elif type(value) == Operators:
            match value:
                case Operators.ADD:
                    self.order = 1
                case Operators.SUB:
                    self.order = 2
                case Operators.MUL:
                    self.order = 3
                case Operators.DIV:
                    self.order = 4

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
                try:
                    return  value1 / value2
                except ZeroDivisionError:
                    return float(-1)

    def evaluate(self):
        if not self.left and not self.right:
            return self.value.get_value()
        elif self.left:
            value1 = self.left.evaluate()
            value2 = self.right.evaluate()
            return self.match_operator(self.value, value1, value2)

    def normalize(self):
        if self.left:
            l_order = self.left.normalize()
        else:
            l_order = 0

        if self.right:
            r_order = self.right.normalize()
        else:
            r_order = 0

        if not self.left and not self.right:
            return self.order

        if l_order < r_order:
            temp = self.left
            self.left = self.right
            self.right = temp

        return self.order


