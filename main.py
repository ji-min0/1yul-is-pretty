from blogcode import submain
from blogcode.post import Post
from blogcode.BoradManager import BoardManager, main as board_main
from blogcode.comment import *
from gamecode.game_main import game_main
from log_setup import creat_log_table

creat_log_table()

def main():
    while True:
        current_user = getattr(submain, 'current_user', None)
        
        print("\n===== 메인 메뉴 =====")
        
        if current_user:
            print("1. 게시글 작성")
            print("2. 게시글 목록 보기")
            print("3. 댓글 작성")
            print("4. 파이썬 게임")
            print("5. 로그아웃")
        else:
            print("1. 회원가입")
            print("2. 로그인")
        
        print("0. 종료")
        command = input("👉 메뉴 선택: ").strip()
        
        if command == "0":
            print("프로그램을 종료합니다.")
            break
        
        if current_user:
            if command == "1":
                Post(current_user)
            elif command == "2":
                board_main()
            elif command == "3":
                comment_main(current_user)
                # comment.execute()
            elif command == "4":
                game_main()
            elif command == "5":
                submain.logout_user()
            else:
                print("⚠ 잘못된 선택입니다.")
        else:
            if command == "1":
                username = input("아이디 입력: ")
                password = input("비밀번호 입력: ")
                submain.register_user(username, password)
            elif command == "2":
                username = input("아이디 입력: ")
                password = input("비밀번호 입력: ")
                submain.login_user(username, password)
            else:
                print("⚠ 잘못된 선택입니다. 로그인 후 이용 가능합니다.")


def manage_user():
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
    main()