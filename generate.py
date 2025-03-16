import random
import equation as eq
import math

class Generator:
    def __init__(self, r, limit):
        self.r = r
        self.limit = limit
        self.depth = math.ceil(self.limit / 2)

    def generate_numberic(self):
        denominator = random.randint(1,self.r)
        numerator = random.randint(0, self.r)
        numberic = eq.Numberic(denominator, numerator)
        return numberic

    def generate_equation_tree(self,depth):
        r = self.r

        if depth == 0:
            value = self.generate_numberic()
            self.limit -= 1
            return eq.EquationNode(value, None, None)
        else:
            op = random.choice(list(eq.Operators))
            node = eq.EquationNode(op, None, None)

            if self.limit >= 0:
                node.add_left_child(self.generate_equation_tree(depth-1))
            else:
                node.add_left_child(None)

            if self.limit >= 0:
                node.add_right_child(self.generate_equation_tree(depth-1))
            else:
                node.add_right_child(None)

            return node

if __name__ == '__main__':
    g = Generator(10, 4)
    tree = g.generate_equation_tree(g.depth)
    tree.traverse()
