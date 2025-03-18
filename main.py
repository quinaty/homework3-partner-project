import generate as ge
import file_processor as fp
import argparse
import sys

def get_cli_arguments():
    parser = argparse.ArgumentParser(description='数学题目生成和批改系统')

    # 互斥组确保只能选择生成或批改
    group = parser.add_mutually_exclusive_group(required=True)

    # 批改模式参数
    group.add_argument('-c', '--check', action='store_true',help='启用批改模式（需配合-e和-a参数使用）')
    parser.add_argument('-e', '--question_file', required='-c' in sys.argv,help='题目文件路径')
    parser.add_argument('-a', '--answer_file', required='-c' in sys.argv,help='答案文件路径')

    # 生成模式参数
    group.add_argument('-g', '--generate', action='store_true',
                       help='启用题目生成模式')
    parser.add_argument('-n', '--number', type=int,
                        help='要生成的题目数量', required='-g' in sys.argv)

    # 公共参数
    parser.add_argument('-r', '--range', type=int, default=10,help='数值范围（默认10）')
    parser.add_argument('-l', '--limit', type=int, default=4,help='操作数数量限制（默认4）')
    parser.add_argument('--grade_file', default=fp.const_grade_path,help='成绩输出文件路径')

    return parser.parse_args()


def proofread_the_answers(question, answer):
    return question.evaluate().get_value() == answer.get_value()

def proofread_the_questions(question_path, answer_path, grade_path):
    questions = fp.question_read(question_path)
    answers = fp.answer_read(answer_path)

    if grade_path is None:
        grade_path = fp.const_grade_path
    grade_file = fp.file_open(grade_path)

    correct_num = 0
    wrong_num = 0
    correct_list = list()
    wrong_list = list()
    for i in range(len(questions)):
        if not proofread_the_answers(questions[i], answers[i]):
            wrong_num += 1
            wrong_list.append(i)
        else:
            correct_num += 1
            correct_list.append(i)

    grade_file.write(f"Correct：{correct_num}(")
    for i in correct_list:
        grade_file.write(str(correct_list[i]+1) + ',')
    grade_file.write(")\n")
    grade_file.write(f"Wrong：{wrong_num}(")
    for i in wrong_list:
        grade_file.write(str(wrong_list[i]+1) + ',')
    grade_file.write(")\n")
    fp.file_close(grade_file)

if __name__ == '__main__':
    args = get_cli_arguments()

    if args.check:
        # 批改答案模式
        proofread_the_questions(args.question_file,
                                args.answer_file,
                                args.grade_file)
    elif args.generate:
        # 生成题目模式
        ge.generate_equations(args.range,
                              args.limit,
                              args.number)








