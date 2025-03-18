import argparse
import re
import equation as eq

const_answer_path = "D:\qe\Documents\PythonProgrammes\homework3\\answer.txt"

# 从命令行读取文件
def read_file_from_args():
    parser = argparse.ArgumentParser(description='从命令行读取文件')

    #分别读取问题、答案文件的路径
    parser.add_argument('question_file',type=str)
    parser.add_argument('answer_file',type=str)

    args = parser.parse_args()
    return [args.question_file, args.answer_file]


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
    question_data = file_read(question_path)
    if question_data is None:
        return None
    else:
        question_list = question_data.split('\n')

    while '' in question_list:
        question_list.remove('')

    pattern1 = re.compile(r'\d+[\'\d/\d]*?')
    pattern2 = re.compile(r'[(+\-*/)]')
    question_set = list()

    for question in question_set:
        num = re.match(pattern1,question)
        operator = re.match(pattern2,question)












