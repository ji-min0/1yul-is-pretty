from gamecode.feature.Data_Loader import GameDataLoading
from gamecode.game_logic import GameLogic
from gamecode.ui_manager import Student
from log_setup import log_event, Action
from blogcode.submain import current_user

def game_main():
    user_id = current_user['name'] if current_user else "Unknown"

    students = {
        1: GameDataLoading(),
        2: Student(),
        3: GameLogic()
    }
    # 게임 시작 로그 추가
    log_event(user_id, Action.GAME_START, "게임 시작")

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
    else: 
        # 모든 문제 완료 후 종료 로그
        log_event(user_id, Action.GAME_END, f"게임 종료 | 모든 문제 완료 | 점수: {students[2].score} | 남은 목숨: {students[2].life}")