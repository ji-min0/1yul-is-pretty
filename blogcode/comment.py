import os, pymysql
from datetime import datetime 
from filteringcode.filter import filter_profanity
# import mysql.connector
# from mysql.connector import Error
# from dbconfig import dbconfig
from log_setup import log_event, Action
# from blogcode.submain import current_user

class Comment:
    def __init__(self, author_id="Unknown"):
        self.post_dir = 'blogcode/posts'
        # author_id가 None이면 "Unknown" 처리
        if author_id is None:
            self.author_id = "Unknown"
        else:
            # 혹시 dict로 들어오는 경우 대비
            if isinstance(author_id, dict):
                self.author_id = author_id.get("name", "Unknown")
            else:
                self.author_id = str(author_id)

        os.makedirs(self.post_dir, exist_ok=True)
        self.existing_files = [f for f in os.listdir(self.post_dir) if f.endswith('.txt') and f.split('.')[0].isdigit()]
        # 데이터베이스 연결 설정
        self.conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'dain8154',
            db = 'hanyul',
            charset = 'utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
       
    # def get_db(self):
    #     try:
    #         conn = mysql.connector.connect(**dbconfig)
    #         return conn
    #     except Error as e:
    #         print(f"연결오류 : {e}")
    #         return None
    
    def show_available_posts(self):
        if not self.existing_files:
            print("댓글을 달 수 있는 게시물이 없습니다.")
            return []
        
        print("\n--- 댓글 작성 가능한 게시물 목록 ---")
        post_info = {}
        
        for filename in sorted(self.existing_files, key=lambda x: int(x.split('.')[0])):
            file_path = os.path.join(self.post_dir, filename)
            post_num = int(filename.split('.')[0])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                title = lines[1].replace('제목: ', '').strip() if len(lines) > 1 else '제목 없음'
                post_info[post_num] = {'filename': filename, 'title': title}
                print(f"[{post_num}] 제목: {title}")
        
        return post_info
    
    def execute(self):  
        """댓글 작성 기능만 제공"""
        self.write_comment()
    
    def write_comment(self):
        post_info = self.show_available_posts()
        
        if not post_info:
            return
        
        while True:
            try:
                post_num = int(input("\n댓글을 작성할 게시물 번호를 입력하세요: "))
                if post_num in post_info:
                    break
                else:
                    print("존재하지 않는 게시물 번호입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요. 다시 시도하세요.")
        
        print(f"\n--- {post_num}번 게시물에 댓글 작성 ---")
        print(f"작성자: {self.author_id}") # 여기는 수정 필요할 듯
        comment_text = input("댓글 내용을 입력하세요: ")
        

        # 욕설 필터링 (댓글)
        filtered_comment = filter_profanity(comment_text)
        print(f"\n➡️ 필터링된 댓글 미리보기: {filtered_comment}")

        # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        

        # 로그 기록 남기기
        log_event(self.author_id, Action.COMMENT, f"게시물ID: {post_num}")

        # database에 저장
        self.insert_comment({"post_id" :post_num, "comment_text" : comment_text, "filtered_comment" : filtered_comment});

    def insert_comment(self, data:dict):
        conn = self.conn
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            with conn.cursor() as cur:
                sql = """INSERT INTO comments(account_id, post_id, content_original, content_filtered, created_at)
                        VALUES (%s, %s, %s, %s, %s)"""
                cur.execute(sql, (self.author_id, data["post_id"], data["comment_text"], data["filtered_comment"], created_at))
                conn.commit()
            print(f"✅ 게시글이 저장되었습니다.")
        finally:    
            # 데이터베이스 연결 종료
            conn.close()


if __name__ == "__main__":
    comment_creator = Comment()
    comment_creator.execute()