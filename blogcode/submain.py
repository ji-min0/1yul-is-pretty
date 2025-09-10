# import json  # JSON 모듈을 사용해 사용자 정보를 파일로 저장/불러오기
import mysql.connector
from mysql.connector import Error
from dbconfig import dbconfig

# 전역 변수
#users = {}        # 모든 사용자 정보 저장
current_user = None   # 현재 로그인한 사용자 ID 저장


dbconfig = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'hanyul'
}

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

    # 사용자 정보 추가
    users[username] = {"password": password, "is_admin": is_admin}
    print(f"✅ {username} 님이 회원가입 완료되었습니다.")
    return True


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
        dbpw, adminv = result
        if dbpw != password:
            print("⚠️ 비밀번호가 틀렸습니다.")
            return False
        current_user = {
            'name': username,
            'is_admin': bool(adminv)
        }
        print(f"👋 {username} 님 환영합니다!")
        return True
    except Error as e:
        print(f"오류처리 : {e}")
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
        print(f"👋 {current_user} 님이 로그아웃 되었습니다.")
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
