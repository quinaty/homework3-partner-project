import enum

class Operators(enum.Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'

    def get_value(self):
        if self == Operators.ADD or self == Operators.SUB:
            return 0
        elif self == Operators.MUL or self == Operators.DIV:
            return 1

class Numberic:
    def __init__(self, denominator, numerator):
        self.denominator = denominator
        self.numerator = numerator

    def get_value(self):
        return self.numerator/self.denominator

    def print_numberic(self):
        if self.denominator == 1:
            return int(self.numerator)
        elif self.numerator == 0:
            return 0

        if self.numerator == self.denominator:
            return 1
        elif self.numerator < self.denominator:
            return str(self.numerator) + '/' + str(self.denominator)
        else:
            x = self.numerator % self.denominator
            y = self.numerator // self.denominator
            if x == 0:
                return str(y)
            else:
                return str(str(y) + '\'' + str(x) + '/' + str(self.denominator))


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

    def print_equation(self,pos = 0,op = 0):
        if self.left:
            self.left.print_equation(0,self.value.get_value())

        if type(self.value) == Numberic:
            if pos == 0 and op == 0:
                print('(',end=' ')
                print(self.value.print_numberic(),end=' ')
            elif pos == 1 and op == 0:
                print(self.value.print_numberic(),end=' ')
                print(')',end=' ')
            else:
                print(self.value.print_numberic(),end=' ')

        else:
           match self.value:
                case Operators.ADD:
                   print('+',end=' ')
                case Operators.SUB:
                    print('-',end=' ')
                case Operators.MUL:
                    print('*',end=' ')
                case Operators.DIV:
                    print('/',end=' ')

        if self.right:
            self.right.print_equation(1,self.value.get_value())


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
        if self.left:
            value1 = self.left.evaluate()
        else:
            value1 = self.value.get_value()

        if self.right:
            value2 = self.right.evaluate()
        else:
            value2 = self.value.get_value()

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

class EquationSet:
    def __init__(self, equation_set,answer_set):
        self.equation_set = equation_set
        self.answer_set = answer_set

    def print_equation_set(self):
        for equation in self.equation_set:
            equation.print_equation()
            print('=',end=' ')
            print(equation.evaluate())
