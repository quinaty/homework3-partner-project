import argparse
import re
import equation as eq

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


def answer_read(answer_file):
    answer_data = file_read(answer_file)
    if answer_data is None:
        return None
    else:
        answer_list = answer_data.split('\n')

    pattern = re.compile(r'\d+[\'\d/\d]*?')
    answer_set = list()

    for answer in answer_list:
        an = re.match(pattern, answer)
        if an is None:
            print("答案格式错误")
            return None
        else:
            an = re.sub(r'[\D]', '', answer)
            an = str(an).split('')
            if len(an) == 1:
                answer_set.append(eq.Numberic(1, int(an[0])))
            elif len(an) == 2:
                answer_set.append(eq.Numberic(int(an[1]), int(an[0])))
            else:
                answer_set.append(eq.Numberic(int(an[2])*int(an[0]),int(an[1])))

    return answer_set




