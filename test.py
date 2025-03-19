import unittest
import tempfile
import os
import equation as eq

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

if __name__ == '__main__':
    unittest.main()