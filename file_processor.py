import argparse
import re
import equation as eq

const_answer_path = "D:\\qe\\Documents\\PythonProgrammes\\homework3\\answer.txt"
const_question_path = "D:\\qe\\Documents\\PythonProgrammes\\homework3\\question.txt"
const_grade_path = "D:\\qe\\Documents\\PythonProgrammes\\homework3\\grade.txt"

# 从命令行读取文件
def read_file_from_args():
    parser = argparse.ArgumentParser(description='从命令行读取文件')

    #分别读取问题、答案文件的路径
    parser.add_argument('question_file','-e' ,type=str)
    parser.add_argument('answer_file','-a',type=str)
    parser.add_argument('grade_file',type=str)

    args = parser.parse_args()
    return [args.question_file, args.answer_file, args.grade_file]


# 读取文件内容
def file_read(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"错误：文件 '{file_path}' 不存在")
    except IsADirectoryError:
        print(f"错误：'{file_path}' 是一个目录")
    except PermissionError:
        print(f"错误：没有权限读取 '{file_path}'")
    except UnicodeDecodeError:
        print("错误：文件编码不支持，请尝试指定其他编码方式")
    except Exception as e:
        print(f"读取文件时发生未知错误：{str(e)}")

    return None

# 写入文件内容
def file_write(file_path, data):

    try:
        with open(file_path, 'a+', encoding='utf-8') as file:
                file.write(data)
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
    except IsADirectoryError:
        print(f"错误：'{file_path}' 是一个目录")
    except PermissionError:
        print(f"错误：没有权限写入 '{file_path}'")
    except UnicodeDecodeError:
        print("错误：文件编码不支持，请尝试指定其他编码方式")
    except Exception as e:
        print(f"写入文件时发生未知错误：{str(e)}")


def file_open(file_path):
    try:
        return open(file_path, 'a+', encoding='utf-8')
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
        return None
    except IsADirectoryError:
        print(f"错误：'{file_path}' 是一个目录")
        return None
    except PermissionError:
        print(f"错误：没有权限写入 '{file_path}'")
        return None
    except UnicodeDecodeError:
        print("错误：文件编码不支持，请尝试指定其他编码方式")
        return None
    except Exception as e:
        print(f"打开文件时发生未知错误：{str(e)}")
        return None

def file_close(file_obj):
    try:
        file_obj.close()
    except Exception as e:
        print(f"关闭文件时发生未知错误：{str(e)}")

def equation_write(equation,file_path,index):
    if not file_path:
        file_path = const_question_path

    file = file_open(file_path)
    file.write(str(index) + '. ')
    equation.print_equation(0, equation.value.get_type(), file)
    file.write('\n')
    file_close(file)


def single_numeric_read(answer_txt):
    pattern = re.compile(r'\d+[\'\d/\d]*?')
    an = re.match(pattern, answer_txt)
    if an is None:
        print("答案格式错误")
        return None
    else:

        if an == '':
            return None

        an = re.sub(r'\D', ' ', answer_txt)
        num_list = an.split()
        if len(num_list) == 1:
            return eq.Numberic(1, int(num_list[0]))
        elif len(num_list) == 2:
            return eq.Numberic(int(num_list[1]), int(num_list[0]))
        else:
            return eq.Numberic(int(num_list[2]), int(num_list[1]) + int(num_list[0]) * int(num_list[2]))


def answer_read(answer_path):
    answer_data = file_read(answer_path)
    if answer_data is None:
        return None
    else:
        answer_list = answer_data.split('\n')
    # 去除空行
    while '' in answer_list:
        answer_list.remove('')

    answer_set = list()

    for answer in answer_list:
        an = single_numeric_read(answer)
        if an:
            answer_set.append(an)
        else:
            continue

    return answer_set

def question_read(question_path):
    # 读取问题文件
    question_data = file_read(question_path)
    if question_data is None:
        return None
    else:
        question_list = question_data.split('\n')
    # 去除空行
    while '' in question_list:
        question_list.remove('')

    pattern = r"""
        \d+'\d+/\d+    # 带分数如 1'1/3
        |\d+/\d+       # 分数如 3/4
        |\d+           # 整数如 12
        |[-+*/()]      # 运算符和括号
    """
    question_set = list()
    # 运算符优先级
    precedence = {'+': 0, '-': 1, '*': 2, '/': 3, '(': -1, ')': -1}

    # 构建表达式树
    for question in question_list:
        qu = re.findall(pattern, question, re.VERBOSE)

        #分离运算符和数字
        tokens = []
        num_stack = []
        op_stack = []
        for token in qu:
            if token not in ['+', '-', '*', '/', '(', ')']:
                tokens.append(single_numeric_read(token))
            else:
                tokens.append(token)
        #使用双栈法构建表达式树
        for token in tokens:
            if isinstance(token, eq.Numberic):
                num_stack.append(eq.EquationNode(token, None, None))#数字直接入栈
            elif token == '(':
                op_stack.append(token)#左括号入栈
            elif token == ')':
                while op_stack[-1] != '(':
                    build_tree(op_stack, num_stack)#右括号出栈，直到左括号
                op_stack.pop()#左括号出栈
            else:
                while op_stack and precedence[op_stack[-1]] >= precedence[token]:
                    build_tree(op_stack, num_stack)#运算符出栈，直到栈空或优先级低于当前运算符
                op_stack.append(token)#当前运算符入栈

        while op_stack:#栈非空时，将剩余运算符出栈，直到栈空
                build_tree(op_stack, num_stack)

        question_set.append( num_stack[0])

    return question_set

# 构建表达式树
def build_tree(op_stack, num_stack):
    op = op_stack.pop()
    right = num_stack.pop()
    left = num_stack.pop()

    operator = None
    match op:
        case '+': operator = eq.Operators.ADD
        case '-': operator = eq.Operators.SUB
        case '*': operator = eq.Operators.MUL
        case '/': operator = eq.Operators.DIV
    num_stack.append(eq.EquationNode(operator, left, right))












