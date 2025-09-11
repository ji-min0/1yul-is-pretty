import os
from typing import List, Dict
from datetime import datetime
from filteringcode.filter import filter_profanity
import pymysql


#?=============================추가한 것들================================
conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'dain8154',
    db = 'hanyul',
    charset = 'utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
#?============^^^=============추가한 것들================================



class Post:
    def __init__(self, author_id: str = "Unknown"):
        self.author_id = author_id['name'] # 작성자 ID 추가
        self.post_name = input("글의 제목을 입력 해주세요: ")
        self.filted_post_name = filter_profanity(self.post_name)
        self.post_text = input("글의 내용을 입력 해주세요: ")
        self.filted_post_text = filter_profanity(self.post_text)
        self.category = self.select_category()  # 카테고리 선택
        self.created_at = datetime.now()
        #! self.post: List[Dict[str, str]] = [] 
        # ! self.post_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S") # 정보 저장소!
        self.display_post()
        #! self.save_to_file()



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
#?=============================추가한 것들================================
        with conn.cursor() as cur:
            sql = """INSERT INTO posts(name, title, content, created_at, category)
                    VALUES (%s, %s, %s, %s, %s)"""
            cur.execute(sql, (self.author_id, self.filted_post_name, self.filted_post_text, self.created_at,self.category))
            conn.commit()
        conn.close()
        print(f"✅ 게시글이 저장되었습니다.")

#?============^^^=============추가한 것들================================
        separator = "-" * 60
        print(f'시간: {self.created_at}')
        print(separator)
        print(f'제목: {self.filted_post_name}')
        print(separator)
        print(f'작성자: {self.author_id}')
        print(separator)
        print(f'내용: {self.filted_post_text}')
        print(separator)
        print(f'카테고리: {self.category}')  # 카테고리 출력
        print(separator)

    #! def save_to_file(self): 
    #!     post_dir = 'blogcode/posts' 



    #!     existing_files = [f for f in os.listdir(post_dir) if f.endswith('.txt')]
    #!     next_num = 1
    #!     if existing_files:
    #!         numbers = []
    #!         for f in existing_files:
    #!             try:
    #!                 num_str = f.split('.')[0]
    #!                 if num_str.isdigit():
    #!                     numbers.append(int(num_str))
    #!             except ValueError:
    #!                 continue
    #!         if numbers:
    #!             next_num = max(numbers) + 1
        
    #!     file_name = f"{next_num}.txt"
    #!     file_path = os.path.join(post_dir, file_name)















