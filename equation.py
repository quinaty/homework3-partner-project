import enum

class Operators(enum.Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'

    def get_value(self):
        #处理叶子节点缺失的情况
        if self == Operators.ADD or self == Operators.SUB:
            return Numeric(1, 0)
        elif self == Operators.MUL or self == Operators.DIV:
            return Numeric(1, 1)

    def get_type(self):
        #获取操作符的优先级
        if self == Operators.ADD:
            return 0
        elif self == Operators.SUB:
            return 1
        elif self == Operators.MUL or self == Operators.DIV:
            return 1

class Numeric:
    def __init__(self, denominator, numerator):
        self.denominator = denominator
        self.numerator = numerator

    def get_value(self):
        try:
            return self.numerator/self.denominator
        except ZeroDivisionError:
            return -1

    def print_numeric(self):
        # 输出真分数形式的数字
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

        # x = self.numerator % self.denominator
        # y = self.numerator // self.denominator
        # return str(str(y) + '\'' + str(x) + '/' + str(self.denominator))


class EquationNode:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right
        self.order = 0

        if type(value) == Numeric:
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

    def print_equation(self,pos = 0,op = 0,file = None):
        #左边算式优先级大于或等于右边算式优先级时，左括号不加
        #左边算式优先级小于右边算式优先级时，左括号加
        if type(self.value) == Operators and op < self.value.get_type() :
            op1 = 0
        else:
            op1 = op

        if self.left:
            self.left.print_equation(0,self.value.get_type() + op1,file)

        #打印操作符与操作数
        if type(self.value) == Numeric:
            output = self.value.print_numeric()
            if pos == 0 and op > 1:
               line = f"( {output} "
            elif pos == 1 and op > 1:
               line = f"{output} ) "
            else:
                line = f"{output} "

            if file:
                file.write(line)
            else :
                print(line,end=' ')

        else:
            operator = self.value.value

            if file:
                file.write(operator+' ')
            else :
                print(operator,end=' ')

        if self.right:
            self.right.print_equation(1,self.value.get_type() + op,file)


    def get_equation_str(self):
        #生成与print_equation相同格式的字符串
        buffer = []

        def _traverse(node, pos=0, op=0):
            if type(node.value) == Operators and op < node.value.get_type():
                op1 = 0
            else:
                op1 = op

            if node.left:
                _traverse(node.left, 0, node.value.get_type() + op1)

            # 处理当前节点
            if type(node.value) == Numeric:
                output = str(node.value.print_numeric())
                if pos == 0 and op > 1:
                    buffer.append(f"( {output} ")
                elif pos == 1 and op > 1:
                    buffer.append(f"{output} ) ")
                else:
                    buffer.append(f"{output} ")
            else:
                buffer.append(f"{node.value.value} ")

            if node.right:
                _traverse(node.right, 1, node.value.get_type() + op)

        _traverse(self)
        return ''.join(buffer).strip().replace('  ', ' ')

    def evaluate(self):
        #递归求值
        if not self.left and not self.right:
            return self.value
        if self.left:
            value1 = self.left.evaluate()
        else:
            value1 = self.value.get_value()

        if self.right:
            value2 = self.right.evaluate()
        else:
            value2 = self.value.get_value()

        # print(
        #     f"操作数1: {value1.numerator}/{value1.denominator} 操作符: {self.value.value} 操作数2: {value2.numerator}/{value2.denominator}")  # 添加调试输出
        result = simplify_fraction_evaluate(value1, value2, self.value)

        if result.get_value() < 0:
            return Numeric(1, -1)
        #对结果进行化简
        common_divisor = greatest_common_divisor(result.numerator, result.denominator)
        if common_divisor != 0:
            result.numerator //= common_divisor
            result.denominator //= common_divisor
        return result

    def compare(self, other_node):
        #比较两个表达式树是否结构相同（考虑交换律）
        if type(self.value) != type(other_node.value):
            return False

        if isinstance(self.value, Numeric):
            return self.value.get_value() == other_node.value.get_value()

        # 对于运算符，检查是否满足交换律
        if self.value in [Operators.ADD, Operators.MUL]:
            return (self.left.compare(other_node.left) and self.right.compare(other_node.right)) or \
                    (self.left.compare(other_node.right) and self.right.compare(other_node.left))
        else:
            return self.left.compare(other_node.left) and self.right.compare(other_node.right)


    def normalize(self):
        #标准化
        #使得左子树的优先级大于右子树的优先级，且左叶子始终大于右叶子
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

        return self.order + l_order + r_order


class EquationSet:
    # 方程集合
    def __init__(self, equation_list, answer_dict):
        self.equation_list = equation_list
        self.answer_dict = answer_dict

    def print_equation_set(self):
        for equation in self.equation_list:
            equation.print_equation(0,equation.value.get_type())
            print('=',end=' ')
            print(self.answer_dict[equation])


#求最大公约数
def greatest_common_divisor(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def simplify_fraction_evaluate(fraction1, fraction2, operator):
    denominator = 1
    numerator1 = 0
    numerator2 = 0
    if operator == Operators.ADD or operator == Operators.SUB:
       # 求最小公倍数
       common_divisor = greatest_common_divisor(fraction1.denominator, fraction2.denominator)
       # 分母通分
       denominator = (fraction1.denominator * fraction2.denominator) // common_divisor

       # 分子通分
       numerator1 = fraction1.numerator * (denominator // fraction1.denominator)
       numerator2 = fraction2.numerator * (denominator // fraction2.denominator)

    if denominator == 0:
        return Numeric(1, -1)

    # 计算结果
    match operator:
        case Operators.ADD:
            return Numeric(denominator, numerator1 + numerator2)
        case Operators.SUB:
            return Numeric(denominator, numerator1 - numerator2)
        case Operators.MUL:
            return Numeric(fraction1.denominator * fraction2.denominator, fraction1.numerator * fraction2.numerator)
        case Operators.DIV:
            if fraction2.numerator == 0:
                return Numeric(1, -1)
            else:
                return Numeric(fraction1.denominator * fraction2.numerator, fraction1.numerator * fraction2.denominator)