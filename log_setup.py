from enum import Enum
from datetime import datetime
import pymysql
from dbconfig import dbconfig

class Action(Enum): 
    SIGNUP = "signup"
    LOGIN = "login"
    LOGOUT = "logout"
    VIEW_POST = "view_post"
    VIEW_POST_LIST = "view_post_list"
    SORT_POST = "sort_post"
    SEARCH_POST = "search_post"
    COMMENT = "comment"
    GAME_START = "game_start"
    GAME_END = "game_end"

def creat_log_table(): 
    try: 
        conn=pymysql.connect(**dbconfig)
        with conn.cursor() as cursor: 
            sql = """
                CREATE TABLE IF NOT EXISTS user_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(255) NOT NULL,
                action VARCHAR(50) NOT NULL,
                detail TEXT,
                timestamp DATETIME NOT NULL
            ) CHARACTER SET utf8mb4;
            """
            cursor.execute(sql)
        conn.commit()
        conn.close()
        print("user_log 테이블 생성 완료")
    except Exception as e:
        print(f"⚠️ 테이블 생성 오류: {e}")

def log_event(user_name: str, action: Action, detail: str = ""): 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try: 
        conn = pymysql.connect(**dbconfig)
        with conn.cursor() as cursor: 
            sql = """
            INSERT INTO user_logs (user_name, action, detail, timestamp)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (user_name, action.name, detail, timestamp))
        conn.commit()
    except Exception as e: 
        print(f"⚠️ 로그 기록 오류: {e}")

if __name__ == "__main__": 
    creat_log_table()