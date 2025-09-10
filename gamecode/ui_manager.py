import sys
# # input 데이터
# input_data = {
#         "numbers" : 1,
#         "level": "1",
#         "questions": "파이썬에서 특정 조건에 따라 코드 블록을 실행할 때 사용하는 키워드는 무엇인가요?",
#         "choices": "A) loop \nB) when \nC) if \nD) while",
#         "answers": "C",
#         "explanations": "if는 파이썬에서 조건을 검사하여 코드 실행 여부를 결정하는 조건문의 시작 키워드입니다.",
#         "correct_answer" : "c"
#     }


class  Student: 

    def __init__(self):
        self.wrong_answer = []
        self.life = 5
        self.score = 0


    # 점수체크 함수
    def scoring(self, data):
        '''
        {'numbers': 1, 
        'level': '2',
        'questions': '다음 while 반복문은 몇 번 "반복"을 출력하나요?\ncount =  0\nwhile count < 2:\n\tprint("반복")\n\tcount += 1', 
        'choices': 'A) 0번 \nB) 1번 \nC) 2번 \nD) 3번
        ', 'answer': 'C', 
        'explanation': 'count가 0일 때, 1일 때 count < 2 조건이 참이 되어 총 두 번 "반복"을 출력합니다. 
        count가 2가 되면 조건이 거짓이 되어 반복문이 종료됩니다.', 'correct_answer': 'A'} 3번쨰 파일
        '''

        # 정답 체크 대소문자가 다를수도 있어서 대문자로 올리고 비교
        if data["answers"].upper().strip() == data["correct_answer"].upper() :
            # 맞으면 점수 1점 상승
            self.score += 1
            # print(f'현재 점수는 {score}점 입니다.')
            return True
        
        else :
            # 틀리면 오답리스트
            self.wrong_answer.append({
                "numbers": data["numbers"],
                "questions": data["questions"],
                "answers": data["answers"],
                "explanations": data["explanations"],
                "choices": data["choices"],
                "correct_answer": data["correct_answer"]
            })

            # 목숨이 0보다 크면 목숨 1 감소
            if self.life > 0 :
                self.life -= 1
                # print(f'남은 목숨은 {life}개 입니다.')
            else:
                print('='*100)
                print('='*100)
                print('='*100)
                self.show_wrong_answer()
                sys.exit()

    # 오답노트 함수 
    def show_wrong_answer(self):
        # 리스트로 받은 오답리스트 돌면서 출력
        for i , w in enumerate(self.wrong_answer,1):
            print(f"틀린 문제 {w['numbers']}번 : {w['questions']}".replace("\\n","\n"))
            print(f"보 기: \n{w['choices']}".replace("\\n","\n"))
            print(f"내 답: {w['answers']} / 정답: {w['correct_answer']}".replace("\\n","\n"))
            print(f"설명: {w['explanations']}".replace("\\n","\n"))
            print()

    def show_left_life(self):
            print('💚 ' * self.life, '\n')
