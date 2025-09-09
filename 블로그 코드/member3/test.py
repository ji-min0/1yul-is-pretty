from typing import List, Dict

class Post:
    def __init__(self):
        self.post_name = input("글의 제목을 입력 해주세요: ")
        self.post_text = input("글의 내용을 입력 해주세요: ")
        self.category = self.select_category()  # 카테고리 선택
        self.post: List[Dict[str, str]] = []  # 정보 저장소
        self.display_post()
        self.save_to_file()

    def select_category(self) -> str: 
        while True:
            try:
                category = int(input("카테고리를 선택하세요 (1.매우 좋음, 2.좋음, 3.그냥저냥, 4.나쁨, 5.매우 나쁨, 6.기타): "))
                if category == 1:
                    return "매우 좋음"
                elif category == 2:
                    return "좋음"
                elif category == 3:
                    return "그냥저냥"
                elif category == 4:
                    return "나쁨"
                elif category == 5:
                    return "매우 나쁨"
                elif category == 6:
                    return "기타"
                else:
                    print("잘못된 선택입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요. 다시 시도하세요.")

    def display_post(self):
        separator = "-" * 60
        print(separator)
        print(f'제목: {self.post_name}')
        print(separator)
        print(f'내용: {self.post_text}')
        print(separator)
        print(f'카테고리: {self.category}')  # 카테고리 출력
        print(separator)

    def save_to_file(self):
        """게시물 정보를 텍스트 파일에 저장합니다."""
        with open('post.txt', 'w', encoding='utf-8') as file:
            file.write(f'제목: {self.post_name}\n')
            file.write(f'내용: {self.post_text}\n')
            file.write(f'카테고리: {self.category}\n')
            file.write('-' * 60 + '\n')

# 게시물 정보를 파일에 저장
post = Post()
post.save_to_file()