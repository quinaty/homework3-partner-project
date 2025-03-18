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


def answer_read(answer_path):
    answer_data = file_read(answer_path)
    if answer_data is None:
        return None
    else:
        answer_list = answer_data.split('\n')
    # 去除空行
    while '' in answer_list:
        answer_list.remove('')

    pattern = re.compile(r'\d+[\'\d/\d]*?')
    answer_set = list()

    for answer in answer_list:
        an = re.match(pattern, answer)
        if an is None:
            print("答案格式错误")
            return None
        else:

            if an == '':
                continue

            an = re.sub(r'\D', ' ', answer)
            num_list = an.split()
            if len(num_list) == 1:
                answer_set.append(eq.Numberic(1, int(num_list[0])))
            elif len(num_list) == 2:
                answer_set.append(eq.Numberic(int(num_list[1]), int(num_list[0])))
            else:
                answer_set.append(eq.Numberic(int(num_list[2]),int(num_list[1]) + int(num_list[0]) * int(num_list[2])))

    return answer_set




