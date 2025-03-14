



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

