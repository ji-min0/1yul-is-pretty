import json  # JSON 모듈을 사용해 사용자 정보를 파일로 저장/불러오기

# 전역 변수
users = {}        # 모든 사용자 정보 저장
current_user = None   # 현재 로그인한 사용자 ID 저장



# 사용자 데이터 저장 함수
def save_data():
    # users 딕셔너리 내용을 users.json 파일로 저장
    with open("users.json", "w", encoding="utf-8") as f:
        # ensure_ascii=False -> 한글 깨짐 방지, indent=2 -> 파일 보기 좋게 들여쓰기
        json.dump(users, f, ensure_ascii=False, indent=2)



# 사용자 데이터 불러오기 함수
def load_data():
    # users.json 파일에서 사용자 정보를 불러와 users 딕셔너리에 저장
    global users
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)  # 파일 내용을 딕셔너리로 변환
    except FileNotFoundError:
        # 파일이 없으면 빈 딕셔너리로 초기화
        users = {}


# 회원가입 함수
def register_user(username, password, is_admin=False):
    # 새로운 사용자를 등록
    # username: 사용자 ID
    # password: 비밀번호
    # is_admin: 관리자 여부 (기본값 False)
    if username in users:
        print("⚠️ 이미 존재하는 사용자입니다.")
        return False

    # 사용자 정보 추가
    users[username] = {"password": password, "is_admin": is_admin}
    print(f"✅ {username} 님이 회원가입 완료되었습니다.")
    return True


# 로그인 함수
def login_user(username, password):
    # 사용자 로그인 - username, password 확인 후 로그인 성공 시 current_user에 저장
    global current_user
    if username not in users:
        print("⚠️ 존재하지 않는 사용자입니다.")
        return False

    if users[username]["password"] != password:
        print("⚠️ 비밀번호가 틀렸습니다.")
        return False

    current_user = username
    print(f"👋 {username} 님 환영합니다!")
    return True


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
    if current_user and users[current_user]["is_admin"]:
        return True
    return False
