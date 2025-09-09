from feature.Data_Loader import GameDataLoading
from game_logic import GameLogic
from ui_manager import Student

# def main():

students = {
    1: GameDataLoading(),
    2: Student(),
    3: GameLogic()
}

# 1. 문제유형 질문
unit_select = students[3].game_settting()

# 2. 그에 맞는 파일 가져오기
questions = students[1].get_all_questions(unit_select)  # 이게 실제 문제 리스트
# all_data = students[1].get_all_data()        # 파일별 그룹화된 데이터 (사용하지 않음)
# processed = students[1].get_all_processed()

# 3. 문제 세팅
students[3].questions_criteria(questions)    # 전역변수 유지

# 4. while문에서의 문제 출제. correct_answer key 추가.
number = 0
while len(students[3].quiz_list) > number :
    # 문제와 정답을 return 받습니다.
    quiz_dict = students[3].show_quiz_input(number)
    if students[3].user_input.strip() == "종료":
        students[2].life = 0
        students[2].show_left_life()
        print('='*100)
        print('='*100)
        print('='*100)
        students[2].show_wrong_answer()
        break
    else:
        students[2].show_left_life()
        students[2].scoring(quiz_dict)

    # 문제를 체점합니다 (종료를 입력받으면 결과 return)

    number += 1
