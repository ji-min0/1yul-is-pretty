from blogCode import submain
from blogCode.post import Post
from blogCode.BoradManager import BoardManager, main as board_main
from blogCode.comment import Comment
from gameCode.game_main import game_main

def main():
    while True:
        print("\n===== 메인 메뉴 =====")
        print("1. 게시글 작성")
        print("2. 게시글 목록 보기")
        print("3. 단어 맞추기 게임")
        print("4. 댓글 작성")
        print("5. 회원 관리 (로그인/회원가입)")
        print("0. 종료")

        command = input("👉 메뉴 선택: ").strip()

        if command == "0":
            print("프로그램을 종료합니다.")
            break
        elif command == "1":
            # 현재 로그인한 사용자 정보 가져오기
            current_user = getattr(submain, 'current_user', None)
            if current_user:
                Post(current_user)
            else:
                print("⚠️ 게시글을 작성하려면 먼저 로그인해주세요.")
                print("회원 관리 메뉴에서 로그인 후 다시 시도해주세요.")
        elif command == "2":
            board_main()

        elif command == "3":
            current_user = getattr(submain, 'current_user', None)
            if current_user:
                main()
                continue
            else:
                print("⚠️ 댓글을 작성하려면 먼저 로그인해주세요.")
                print("회원 관리 메뉴에서 로그인 후 다시 시도해주세요.")


        elif command == "4":
            # 댓글 작성 기능
            current_user = getattr(submain, 'current_user', None)
            if current_user:
                comment = Comment(current_user)
                comment.execute()
            else:
                print("⚠️ 댓글을 작성하려면 먼저 로그인해주세요.")
                print("회원 관리 메뉴에서 로그인 후 다시 시도해주세요.")

        elif command == "5":
            manage_user()
        else:
            print("⚠ 잘못된 명령어입니다.")

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
    submain.load_data()
    main()
    submain.save_data()