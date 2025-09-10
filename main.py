from blogcode import submain
from post import Post
from blogcode.BoradManager import BoardManager, main as board_main
from comment import Comment
from gamecode.gmmain import gm_main

def main():
    # 메인 메뉴 진입 전 LogIn/SignUp 먼저 진행
    current_user = login_or_signup()

    while True:
        print("\n===== 메인 메뉴 =====")
        print("1. 게시글 작성")
        print("2. 게시글 목록 보기")
        print("3. 댓글 작성")
        print("4. 파이썬 게임")
        print("0. 종료")

        command = input("👉 메뉴 선택: ").strip()

        if command == "0":
            print("프로그램을 종료합니다.")
            break
        elif command == "1":
                Post(current_user)
        elif command == "2":
            board_main()
        elif command == "3": 
            comment = Comment(current_user)
            comment.execute()
        elif command == "4":
                game_main()
        else:
            print("⚠️ 잘못된 명령어입니다.")

def login_or_signup(): 
    while True: 
        print("\n--- 회원 관리 ---")
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 로그아웃")
        print("0. 메인으로 돌아가기")

        choice = input("👉 선택: ").strip()

        if choice == "1":
            username = input("아이디 입력: ")
            password = input("비밀번호 입력: ")
            submain.register_user(username, password)
            submain.save_data()
        elif choice == "2":
            username = input("아이디 입력: ")
            password = input("비밀번호 입력: ")
            submain.login_user(username, password)
        elif choice == "3":
            submain.logout_user()
        elif choice == "0":
            break
        else:
            print("⚠ 잘못된 선택입니다.")

if __name__ == "__main__":
    submain.load_data()
    main()
    submain.save_data()