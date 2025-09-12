import os
from datetime import datetime 
from filteringcode.filter import filter_profanity
# import mysql.connector
# from mysql.connector import Error
# from dbconfig import dbconfig
from log_setup import log_event, Action
from dbconfig import dbconfig
import pymysql

def get_connection():
    return pymysql.connect(
        host=dbconfig['host'],
        user=dbconfig['user'],
        password=dbconfig['password'],
        db=dbconfig['database'],
        charset=dbconfig['charset'],
        cursorclass=pymysql.cursors.DictCursor
    )

class Comment:
    def __init__(self, user_id=None):
        self.user_id = user_id['name']
    
    def posts(self):

        conn = get_connection()
        with conn.cursor() as cur:
            sql = """SELECT id ,name, title, content, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at, category
        FROM posts;"""
            cur.execute(sql)
            datas = cur.fetchall()
        conn.close()
        return datas

    def show_available_posts(self):
        datas = self.posts()
        print('📃 ==댓글 작성 가능한 게시글 목록== 📃')

        for data in datas:
            print(f"{data['id']}. {data['title']} (작성자: {data['name']}, 시간: {data['created_at']})")
            print('-'*60)
    def write_comment(self):

        while True:
            try:
                post_num = int(input("\n댓글을 작성할 게시물 번호를 입력하세요: "))
                datas = self.posts()
                for data in datas:
                    if post_num == data['id']:
                        print(f"\n--- {post_num}번 게시물에 댓글 작성 ---")
                        print(f"작성자: {data['name']}") 
                        comment_text = input("댓글 내용을 입력하세요: ")
                        filtered_comment = filter_profanity(comment_text)
                        print(f"\n➡️ 필터링된 댓글 미리보기: {filtered_comment}")
                        conn = get_connection()
                        with conn.cursor() as cur:
                            sql = """INSERT INTO comments(account_id, post_id, content_original, content_filtered, created_at)
                                    VALUES (%s, %s, %s, %s, %s)"""
                            cur.execute(sql, (self.user_id, data['id'], comment_text, filtered_comment, datetime.now()))
                            conn.commit()
                        log_event(self.user_id, Action.COMMENT, f"게시물ID: {post_num}")
                        conn.close()
                        return
                else:
                    Comment.show_available_posts(self)
                    print("존재하지 않는 게시물 번호입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요. 다시 시도하세요.")

def comment_main(user_id):
    cm = Comment(user_id)
    cm.show_available_posts()
    cm.write_comment()
