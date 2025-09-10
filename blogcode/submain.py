# import json  # JSON 모듈을 사용해 사용자 정보를 파일로 저장/불러오기
import mysql.connector
from mysql.connector import Error
from dbconfig import dbconfig
from log_setup import log_event, Action

# 전역 변수
#users = {}        # 모든 사용자 정보 저장
current_user = None   # 현재 로그인한 사용자 ID 저장


def get_db():
    try:
        conn = mysql.connector.connect(**dbconfig)
        return conn
    except Error as e:
        print(f"연결오류 : {e}")
        return None



# 회원가입 함수
def register_user(username, password, is_admin=False):
    # 새로운 사용자를 등록
    # username: 사용자 ID
    # password: 비밀번호
    # is_admin: 관리자 여부 (기본값 False)
    admin = 1 if is_admin else 0
    conn =  get_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM accounts WHERE name = %s", (username,))
        if cursor.fetchone():
            print("⚠️ 이미 존재하는 사용자입니다.")
            return False
        sql = "INSERT INTO accounts (name, password, admin) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, password, admin))
        conn.commit()
        
        # log 기록
        log_event(username, Action.SIGNUP, f"admin 여부: {is_admin}")
        return True
    except Error as e:
        print(f"오류처리 : {e}")
        conn.rollback()
        return False

# 로그인 함수
def login_user(username, password):
    # 사용자 로그인 - username, password 확인 후 로그인 성공 시 current_user에 저장
    global current_user

    conn = get_db()
    if not conn: return False
    cursor = conn.cursor()
    try:
        sql = "SELECT password, admin FROM accounts WHERE name = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result is None:
            print("⚠️ 존재하지 않는 사용자입니다.")
            return False
        dbpw, admin = result
        if dbpw != password:
            print("⚠️ 비밀번호가 틀렸습니다.")
            return False
        current_user = {
            'name': username,
            'is_admin': bool(admin)
        }
        print(f"👋 {username} 님 환영합니다!")

        # log 기록
        log_event(username, Action.LOGIN)
        return True
    except Error as e:
        print(f"오류처리 : {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
        


# 로그아웃 함수
def logout_user():
    # 현재 로그인한 사용자를 로그아웃
    # current_user를 None으로 초기화
    global current_user
    if current_user:
        username = current_user['name']
        print(f"👋 {username} 님이 로그아웃 되었습니다.")

        # log 기록
        log_event(username, Action.LOGOUT)
        current_user = None
    else:
        print("⚠️ 현재 로그인한 사용자가 없습니다.")


# 관리자 확인 함수
def is_admin():
    # 현재 로그인한 사용자가 관리자 권한이 있는지 확인
    # True/False 반환
    if current_user and current_user['is_admin']:
        return True
    return False
