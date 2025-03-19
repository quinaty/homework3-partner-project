import unittest
import tempfile
import os
import equation as eq
import generate as ge
import file_processor as fp
import main as m

# 导入需要测试的函数
from file_processor import (
    file_read,
    file_write,
    single_numeric_read,
    answer_read,
    question_read,
    build_tree
)

class TestFileRead(unittest.TestCase):
    def test_read_existing_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmp:
            tmp.write("test content")
            tmp_path = tmp.name
        self.assertEqual(file_read(tmp_path), "test content")
        os.remove(tmp_path)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            file_read("nonexistent_file.txt")

    def test_read_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertIsNone(file_read(tmpdir))

class TestFileWrite(unittest.TestCase):
    def test_append_to_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmp:
            tmp_path = tmp.name
        file_write(tmp_path, "new data")
        with open(tmp_path, 'r', encoding='utf-8') as f:
            self.assertIn("new data", f.read())
        os.remove(tmp_path)

class TestSingleNumericRead(unittest.TestCase):
    def test_integer(self):
        num = single_numeric_read("5")
        self.assertEqual(num.numerator, 5)
        self.assertEqual(num.denominator, 1)

    def test_fraction(self):
        num = single_numeric_read("3/4")
        self.assertEqual(num.numerator, 3)
        self.assertEqual(num.denominator, 4)

    def test_mixed_number(self):
        num = single_numeric_read("1'1/3")
        self.assertEqual(num.numerator, 4)
        self.assertEqual(num.denominator, 3)

    def test_invalid_format(self):
        self.assertIsNone(single_numeric_read("invalid"))

class TestAnswerRead(unittest.TestCase):
    def test_answer_parsing(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmp:
            tmp.write("1. 5\n2. 3/4\n3. 1'1/3\n")
            tmp_path = tmp.name
        answers = answer_read(tmp_path)
        self.assertEqual(len(answers), 3)
        self.assertEqual(answers[0].numerator, 5)
        self.assertEqual(answers[1].denominator, 4)
        os.remove(tmp_path)

class TestQuestionRead(unittest.TestCase):
    def test_expression_parsing(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmp:
            tmp.write("1. 3 + 4 * 2\n")
            tmp_path = tmp.name
        questions = question_read(tmp_path)
        self.assertEqual(len(questions), 1)
        # 假设EquationNode有evaluate方法
        result = questions[0].evaluate()
        self.assertEqual(result.numerator, 11)
        os.remove(tmp_path)

class TestBuildTree(unittest.TestCase):
    def test_build_addition_tree(self):
        op_stack = ['+']
        num_stack = [
            eq.EquationNode(eq.Numberic(1, 3), None, None),
            eq.EquationNode(eq.Numberic(1, 4), None, None)]
        build_tree(op_stack, num_stack)
        self.assertEqual(len(num_stack), 1)
        self.assertEqual(num_stack[0].value, eq.Operators.ADD)


class TestGenerate(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_files = {
            'question.txt': '',
            'answer.txt': '',
            'exercise.txt': '',
        }
        for filename, content in self.test_files.items():
            path = os.path.join(self.test_dir.name, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

    def test_generate(self):
        question_path = os.path.join(self.test_dir.name, 'question.txt')
        answer_path = os.path.join(self.test_dir.name, 'answer.txt')
        exercise_path = os.path.join(self.test_dir.name, 'exercise.txt')

        es = ge.generate_equations(10, 4, 2,exercise_path)
        es.print_equation_set()
        for answer in es.answer_dict.values():
            fp.file_write(answer_path, str(answer) + '\n')

        n = 0
        for equation in es.equation_list:
            fp.equation_write(equation, question_path, n)
            n += 1

        self.clean_up()

    def clean_up(self):
        self.test_dir.cleanup()

class TestProofs(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_files = {
            'question.txt': """12. 1 / 1/8 + 1 + 1/2
13. 4 - 2 + 1'1/2 + 0
14. ( 5 * 3 ) * ( 8 - 0 )
15. 7 + 0 + 2/3 + 2/7
16. ( 4 * 1 ) * ( 7 + 2 )""",
            'answer.txt': """11.  3
12.  9'1/2
13.  3'1/2
14.  120
15.  7'20/21""",
            'grade.txt': '',
        }
        for filename, content in self.test_files.items():
            path = os.path.join(self.test_dir.name, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

    def test_proofs(self):
        question_path = os.path.join(self.test_dir.name, 'question.txt')
        answer_path = os.path.join(self.test_dir.name, 'answer.txt')
        grade_path = os.path.join(self.test_dir.name, 'grade.txt')

        m.proofread_the_questions(question_path, answer_path, grade_path)

        file_data = fp.file_open(grade_path)
        print(file_data.read())
        fp.file_close(file_data)

        self.test_dir.cleanup()


if __name__ == '__main__':
    unittest.main()