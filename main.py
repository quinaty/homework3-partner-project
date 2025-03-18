import equation as eq
import file_processor as fp
def proofread_the_answers(question, answer):
    return question.evaluate().get_value() == answer.get_value()

def proofread_the_questions(question_path, answer_path, grade_path):
    questions = fp.question_read(question_path)
    answers = fp.answer_read(answer_path)
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
        grade_file.write(str(correct_list[i]) + ',')
    grade_file.write(")\n")
    grade_file.write(f"Wrong：{wrong_num}(")
    for i in wrong_list:
        grade_file.write(str(wrong_list[i]) + ',')
    grade_file.write(")\n")
    fp.file_close(grade_file)

if __name__ == '__main__':
    parser = fp.argparse.ArgumentParser()






