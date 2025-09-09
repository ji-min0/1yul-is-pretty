from random import shuffle
import sys, time, threading

class  GameLogic: 

    def __init__(self):        
        self.quiz_list = [] # 출제할 문제리스트 저장
        self.keys = ['level', 'questions', 'choices', 'answer', "explanation"]
        self.level = ("1", "2", "3")
        self.units = ("1", "2", "3", "4")

        self.criteria_select = ""
        self.level_select = ""

    
    def game_settting(self):
        '''
        1. 게임 방식을 정합니다. 
        2. 문제 출제 유형을 정확히 선택했는지 검증합니다.
        '''
        # =======================================================================
        print("  📚 파이썬 Q&A 학습 게임 퀴즈 📚")
        print("  🎯 ❤️ 를 모두 잃으면 게임이 종료됩니다! (5개 제공)🎯")
        print("  🚀 목차입니다. \n\t1. 변수와 데이터 타입 "
        "\n\t2. 자료구조 기초 " \
        "\n\t3. 조건문과 반복문" \
        "\n\t4. 함수와 예외처리")
        criteria = ("레벨별", "단원별", "전체")
        criteria_select = input("🕹️문제 유형을 선택해주세요!(전체, 레벨별, 단원별)").strip()
        # =======================================================================
        
        self.criteria_select = GameLogic.exact_value(criteria_select, criteria, "'전체', '레벨별', '단원별'")    # 입력값 검증.
        
        unit_select:str = "0"
        if self.criteria_select == "단원별":
            # unit_select = input("⍰ 단원은 4개로 구성되어 있습니다. 원하시는 단윈의 숫자를 입력해주세요. (1, 2, 3, 4) ⍰").strip() # 입력값
            unit_select = GameLogic.exact_value(input("⍰ 단원은 4개로 구성되어 있습니다. 원하시는 단윈의 숫자를 입력해주세요. (1, 2, 3, 4) ⍰").strip()
                                                , self.units, "1, 2, 3, 4") # 검증

        return unit_select
    

    def questions_criteria(self, quiz_list):
        '''
        1. 받은 문제를 유형에 맞춰 리스트를 구성합니다.
        @return: 출제할 문제를 반환합니다. 
        '''
        self.quiz_list = quiz_list
        # 정답을 입력과 순서성을 가져야함으로 list구조 유지.
        if self.criteria_select in ("전체", "단원별"): 
            self.quiz_list = GameLogic.shuffle_numbering(quiz_list)  # 셔플 맟 순서값 부여
            return self.quiz_list
        
        elif self.criteria_select == "레벨별": 
            level_index = self.keys.index("level")
            leval_select = input("⍰ 레벨은 3단계로 이루어져 있습니다. 원하시는 레벨을 입력해주세요. (1, 2, 3) ⍰").strip() # 입력값
            self.leval_select = GameLogic.exact_value(leval_select, self.level, "1, 2, 3") # 검증

            level_list = [item for item in self.quiz_list if str(item.get("level")) == self.leval_select] # 선택값 list
            self.quiz_list = GameLogic.shuffle_numbering(level_list)  # 셔플 맟 순서값 부여
            return self.quiz_list


    def exact_value(select_values, exact_list, messages):
        '''
        문제 출제 유형을 정확히 선택했는지 검증합니다.
        Parameter : 검증값, 검증기준값, 오류메세지
        '''
        if select_values == "종료":
            sys.exit()
        elif select_values not in exact_list:
             while True:
                # 올바른 입력을 받을 때까지 반복합니다. 
                print("⚠️ 잘못된 유형입니다. ",messages,"중 하나를 입력하세요.")
                select_values = input("🕹️다시 입력해주세요: ").strip()
                if select_values in exact_list:
                    return select_values
        else :
            return select_values


    def shuffle_numbering(shuffle_list):
        '''
        주어진 문제 list를 섞고 순서를 메깁니다.
        '''
        shuffle(shuffle_list)
        return [{'numbers':i, **sublist} for i, sublist in enumerate(shuffle_list, start=1)]   # numbers key add
    
    def show_quiz_input(self, number:int=0) -> dict:
        '''
        주어진 시간(timeout) 내에 사용자 입력을 받는 함수.
    
        timeout: 입력을 기다릴 시간(120초).
        return: 사용자 입력 문자열 또는 None을 포함한 dictionary.
        1. 문제를 보여줍니다.
        2. 정답을 입력받습니다.
        '''
        timeout = 120
        self.user_input = None
        quiz = self.quiz_list[number]
        #===========================================================================================
        def get_input_thread():
            try:
                # 사용자에게 입력을 기다립니다.
                print(f"  🎯 문제당 제한시간은 {timeout//60}분입니다 🎯")
                print(f'{quiz["numbers"]}. {quiz["questions"]}\n{quiz["choices"]}'.replace("\\n","\n"))
                self.user_input = input()
            except EOFError:
                self.user_input = None
    
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