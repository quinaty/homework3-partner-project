import random
import enum
import equation as eq




def generate_numberic(r):
    denominator = random.randint(0, r)
    numerator = random.randint(1, r)
    numberic = eq.Numberic(denominator, numerator)
    return numberic

def generate_expression(value,is_root=False):
    rootlist = [eq.Brackets.LEFT,eq.Brackets.NULL]
    operator = eq.Operators.ADD
    bracket = random.choice(rootlist)

    if not is_root:
        operator = random.choice(list(eq.Operators))
        bracket = random.choice(list(eq.Brackets))

    exp = eq.Expression(value, operator, bracket)
    return exp

def generate_expression_node(r):
    node = eq.EquationTree(generate_expression(generate_numberic(r)), None, None)
    return node

def node_add(node, current, parent):
    if node.expn.operator == eq.Operators.ADD or node.expn.operator == eq.Operators.SUB or (
            parent and parent.expn.bracket == eq.Brackets.RIGHT):
        current.add_right_child(node)
    else:
        if node.expn.operator == eq.Operators.MUL or node.expn.operator == eq.Operators.DIV or (
                node and node.expn.bracket == eq.Brackets.LEFT):
            current.add_left_child(node)


def bracket_check(node, stack, remain_num):
    if node.expn.bracket == eq.Brackets.RIGHT and stack.is_empty():
       return False
    if node.expn.bracket == eq.Brackets.LEFT and remain_num == 1:
        return False

   # print(stack.length(), remain_num)

    required_num = stack.length()
    probability = random.random()
    if probability < required_num/remain_num:
        node.expn.bracket = eq.Brackets.RIGHT

    return True


def generate_equation_tree(r,limit = 4):
    root = eq.EquationTree(generate_expression(generate_numberic(r), True),None,None)
    current = root
    expression_count = 1
    stack = eq.Brackets_Stack()
    if root.expn.bracket == eq.Brackets.LEFT:
        stack.push('(')

    while expression_count < limit :

        node = generate_expression_node(r)

        if bracket_check(node, stack, limit - expression_count):
            if node.expn.bracket == eq.Brackets.LEFT:
                stack.push('(')
            if node.expn.bracket == eq.Brackets.RIGHT and not stack.is_empty():
                stack.pop()

            if expression_count == 0:
                current.parent = root
            else:
                node.parent = current

            node_add(node, current, current.parent)


            if not current.right is None:
                current = node
            expression_count += 1

        else:
            continue

    return root


if __name__ == '__main__':
    r = 10
    equation = generate_equation_tree(r)
    equation.traverse()
    print(equation.evaluate())
