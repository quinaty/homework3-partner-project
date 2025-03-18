import random
import equation as eq
import math
import file_processor as fp

class Generator:
    def __init__(self, r, limit):
        self.r = r
        self.limit = limit
        self.depth = math.ceil(self.limit / 2)

    #生成数字
    def generate_numberic(self):
        denominator = random.randint(1,self.r)
        numerator = random.randint(0, self.r)
            #提高整数的生成概率
        if random.random() < 0.7:
            denominator = 1

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

def generate_equations(r, limit,n):

    equation_set = list()
    answer_set = dict()
    g = Generator(r, limit)

    i = 0
    while i < n:
        depth = g.depth
        g.limit = limit
        tree = g.generate_equation_tree(depth)
        tree.normalize()
        answer = tree.evaluate()
        if answer.get_value() > 0:
            equation_set.append(tree)
            answer_set[tree] = answer.print_numberic()
            i += 1

    es = eq.EquationSet(equation_set, answer_set)
    return es


if __name__ == '__main__':
        es = generate_equations(10, 4, 2)
       # es.print_equation_set()
        for answer in es.answer_dict.values():
            fp.file_write(fp.const_answer_path, str(answer)+'\n')

        for equation in es.equation_list:
            fp.equation_write(equation, fp.const_question_path)

        questions = fp.question_read(fp.const_question_path)
        for question in questions:
            question.print_equation(0, question.value.get_type())
            print('\n')

        # for answer in fp.answer_read(fp.const_answer_path):
        #     print(answer.print_numberic())
