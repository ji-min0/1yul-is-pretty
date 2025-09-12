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
    # 문제 유형별 함수 (텍스트로 변경 필요)
    selects = {
        "전체"      : "get_all_questions",
        "레벨"      : "get_level_questions",
        "단원"      : "get_chapter_questions",
        "setting"  : "get_setting_questions"
    }

    # 게임 시작 로그 추가
    log_event(user_id, Action.GAME_START, "게임 시작")

    # 1. 레벨과 단원 정보 가져와서 로직단에 넘기기
    # 딕셔너리에 저장된 텍스트로 함수를 동적으로 호출
    menu_dict = getattr(students[1],  selects["setting"])()
    students[3].chapters_name = menu_dict["chapter"]
    students[3].levels = menu_dict["level"]
    # 2. 문제유형 질문
    students[3].game_setting()

    # 2-1. 받아온 숫자를 데이터 로더단에 전달
    user_select = students[3].user_select           # 숫자(단원 또는 레벨)
    students[1].user_type = user_select


    # 3. 그에 맞는 파일 가져와서 로직단에 넘기기
    criteria_select = students[3].criteria_select   # 유형
    questions = getattr(students[1],  selects[criteria_select])()
    students[3].quiz_list = questions

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


if __name__ == "__main__":
    loader = game_main()
    