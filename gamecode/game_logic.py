from random import shuffle
import sys, time, threading

class  GameLogic: 

    def __init__(self, level_tuple:tuple = ("1", "2", "3"), chapters_name:tuple = ("1. 변수와 데이터 타입", "2. 자료구조 기초", "3. 조건문과 반복문", "4. 함수와 예외처리")):
        self.quiz_list = []
        self.chapters_name = chapters_name
        self.levels = level_tuple
        self.chapters = tuple(num[0:1] for num in chapters_name)

        self.criteria_select:str = ""   # mode
        self.user_select:str = "0"  # 레벨 또는 단원
        self.user_input:str = ""    # 정답입력

    
    def game_setting(self):
        '''
        1. 게임 방식을 정합니다. 
        2. 문제 출제 유형을 정확히 선택했는지 검증합니다.
        '''
        # =======================================================================
        print("  📚 파이썬 Q&A 학습 게임 퀴즈 📚")
        print("  🎯 ❤️ 를 모두 잃으면 게임이 종료됩니다! (5개 제공)🎯")
        print("  🚀 목차입니다.\n\t", "\n\t ".join([item for item in self.chapters_name]))

        criteria = ("전체", "레벨", "단원")
        criteria_select = input(f"\n🕹️문제 유형을 선택해주세요! {criteria}").strip()
        # =======================================================================
        self.exact_value(criteria_select, criteria, criteria)    # 입력값 검증.
        self.criteria_select = self.user_select
        self.user_select = "0"
        
        if self.criteria_select == "단원":
            self.exact_value(input(f"⍰ {self.criteria_select}은 {len(self.chapters)}개로 구성되어 있습니다. 원하시는 {self.criteria_select}의 숫자를 입력해주세요. {self.chapters} ⍰").strip()
                                                     , self.chapters,  self.chapters) # 검증
        elif self.criteria_select == "레벨": 
            self.exact_value(input(f"⍰ {self.criteria_select}은 {len(self.levels)}단계로 이루어져 있습니다. 원하시는 {self.criteria_select}의 숫자를 입력해주세요. {self.levels} ⍰").strip()
                                                     , self.levels, self.levels) # 검증

    def exact_value(self, select_values, exact_list, messages):
        '''
        문제 출제 유형을 정확히 선택했는지 검증합니다.
        Parameter : 검증값, 검증기준값, 오류메세지
        '''
        if select_values == "종료":
            self.user_select = select_values
        elif select_values not in exact_list:
             while True:
                # 올바른 입력을 받을 때까지 반복합니다. 
                print(f"⚠️ {select_values}는 잘못된 유형입니다. {messages}중 하나를 입력하세요.")
                select_values = input("🕹️다시 입력해주세요: ").strip()
                if select_values in exact_list:
                    self.user_select = select_values
                    break
        else :
            self.user_select = select_values

    def show_quiz_input(self, number:int=0) -> dict:
        '''
        주어진 시간(timeout) 내에 사용자 입력을 받는 함수.
    
        timeout: 입력을 기다릴 시간(120초).
        return: 사용자 입력 문자열 또는 None을 포함한 dictionary.
        1. 문제를 보여줍니다.
        2. 정답을 입력받습니다.
        '''
        timeout = 120
        self.user_input = ""
        quiz = self.quiz_list[number]
        #===========================================================================================
        def get_input_thread():
            try:
                # 사용자에게 입력을 기다립니다.
                print(f"  🎯 문제당 제한시간은 {timeout//60}분입니다 🎯")
                print(f'{quiz["numbers"]}. {quiz["questions"]}\n{quiz["choices"]}'.replace("\\n","\n").replace("\\t","\t"))
                self.user_input = input()
            except EOFError:
                self.user_input = ""
    
        # 입력 스레드를 시작합니다.
        input_thread = threading.Thread(target=get_input_thread)
        input_thread.daemon = True # 메인 스레드 종료 시 함께 종료되도록 설정
        input_thread.start()

        # 입력 스레드가 끝날 때까지 기다리거나, 타임아웃까지 기다립니다.
        input_thread.join(timeout)

        # 타임아웃이 발생했는지 확인합니다.
        if input_thread.is_alive():
            print("\n시간 초과! 제출하지 않은값은 반영되지 않습니다.")
            return None
        else:
            quiz["correct_answer"] = self.user_input.strip() # dict에 사용자 입력값 저장
            return quiz
        #===========================================================================================

if __name__ == "__main__":
    loader = GameLogic()
    loader.game_setting()