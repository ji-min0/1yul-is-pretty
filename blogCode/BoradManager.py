# 포스팅하면 텍스트 파일이 한 파일에 모이고
# 포스팅 하는 포멧이 고정되어 있다는 전제로 코드를 만들었습니다.
# 코드에 주석처리 해놨으니 읽어주세요.

import os
import datetime

folder_path = 'member2/test_posts' # 포스팅한 글을 모아둔 기본 폴더주소

class BoardManager:

    def get_titles_from_post(): # 포스팅한 글을 가져오는 함수
        print('📃 ==게시글 목록== 📃')
        posts = [] #search_content를 위한 리스트 밑으로 계속 나옵니다 분명 이렇게 일일이 안써도 될거 같은데... 가장 확실해서 반복했습니다.
        i = 0
        for filename in os.listdir(folder_path): # 폴더 안에 있는 파일을의 이름을 가져와서 위의 기본 폴더 주소와 합쳐 파일을 열 수 있게 했습니다.
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        
                        if line.startswith("시간: "): # 시간:으로 시작하는 라인을 찾아옵니다.
                            time = line.split(':', 1)[1].strip()
                        elif line.startswith('제목:'):  # '제목:'으로 시작하는 줄을 찾아서 제목 추출
                            title = line.split(':', 1)[1].strip()# 콜론(:) 뒤의 문자열을 가져와 공백 제거
                        elif line.startswith('작성자:'):
                            Writer = line.split(':', 1)[1].strip()
                            print("=" * 60)
                            print (f'{i+1}.제목:{title}\n 시간:{time}\n 작성자:{Writer}')
                            posts.append((title, filename)) #search_content를 위한 리스트 매핑 위에 posts 리스트에 넣게 됩니다 <- 이것도 반복됩니다.
                            i += 1
                            break
            except Exception as e:
                print(f"❗️ 처리 중 오류 발생: {e}")

        return posts #search_content에 posts 정보를 보냄
    
    def Category_search_titles(Category): # 카테고리를 입력하면 그 카테고리를 가지고 있는 포스트들을 긁어오는 함수입니다.
        print(f'🏷️ ==카테고리가 {Category}인 게시글 목록== 🏷️')
        i = 0
        posts = [] #search_content를 위한 리스트
        found = False
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        if line.startswith("제목: "): # 제목을 먼저 title로 가져오는 코드입니다.
                            title = line.split(':', 1)[1].strip()
                        elif line.startswith(f'카테고리: {Category}'): # 이후에 적어 놓은 카테고리와 같은 카테고리를 가진 포스트면 밑의 프린트를 출력합니다.
                                print("=" * 60)
                                print (f'{i + 1}. 제목: {title} 카테고리:{Category}')
                                i += 1
                                posts.append((title, filename)) #search_content를 위한 리스트 매핑
                                found = True
                                break
            except Exception as e:
                print(f"❗️ 처리 중 오류 발생: {e}")

        if not found: # 모든 파일을 다 확인한 후 카테고리에 해당하는 글이 없으면 출력됩니다.
            print('찾으시는 카테고리에 해당하는 글이 없습니다.')
        return posts #search_content에 posts 정보를 보냄
    
    def Latest_post(): # 글을 최신순으로 정렬하는 함수
        print('⏰ ==게시글 최신순으로 정렬== ⏰')
        posts_time_and_title = {} # 글안에 제목과 시간을 딕셔너리 형태로 가져옵니다.
        filename_map = {}  #search_content를 위한 리스트
        i = 0
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        if line.startswith("시간: "): # 시간:으로 시작하는 라인을 찾아옵니다.
                            time = line.split(':', 1)[1].strip()
                        elif line.startswith("제목: "): # 제목을 가져와 title로 가져옵니다.
                            title = line.split(':', 1)[1].strip()
                            filename_map[title] = filename  #search_content를 위한 리스트 매핑
                            try:
                                post_time = datetime.datetime.strptime(time, "%Y.%m.%d %H:%M:%S") # 시간을 datetime.datetime.strptime를 사용해 객체로 만들어 뒤에 sorted로 비교할 수 있게 만들었습니다. 
                                posts_time_and_title[title] = post_time # 제목과 시간을 posts로 딕셔너리 형태로 넣습니다.
                            except Exception as e:
                                print(f"❗️ 처리 중 오류 발생: {e}")
            except Exception as e:
                print(f"❗️ 처리 중 오류 발생: {e}")

        sorted_items_by_value = sorted(posts_time_and_title.items(), key=lambda item: item[1], reverse=True) #posts안의 item[1]즉 시간을 기준으로 정렬하라는 내용입니다.
        
        posts = [] #search_content를 위한 리스트
        for title, time in sorted_items_by_value:
            date_string = time.strftime("%Y.%m.%d %H:%M:%S") # 시간을 다시 strftime로 지정한 포멧을 바꾸어 str로 바꿉니다.
            print("=" * 60)
            print(f'{i + 1}.제목: {title}')
            print(f'시간: {date_string}')
            posts.append((title, filename_map[title]))
            i += 1
        return posts #search_content에 posts 정보를 보냄
    
        
    def Most_liked_post(): # 글을 좋아요순으로 정렬하는 함수
        print('👍 ==게시글 좋아요 순으로 정렬== 👍')
        posts_liked_and_title = {} 
        filename_map = {} #search_content를 위한 리스트
        i = 0
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        if line.startswith("제목: "): # 제목을 가져와 title로 가져옵니다.
                            title = line.split(':', 1)[1].strip()
                        elif line.startswith("좋아요: "): # 좋아요:으로 시작하는 라인을 찾아옵니다.
                            liked = line.split(':', 1)[1].strip()
                            posts_liked_and_title[title] = liked # 제목과 시간을 posts로 딕셔너리 형태로
                            filename_map[title] = filename #search_content를 위한 리스트
            except Exception as e:
                print(f"❗️ 처리 중 오류 발생: {e}")
        
        sorted_items_by_value = sorted(posts_liked_and_title.items(), key=lambda item: item[1], reverse=True)
        
        posts = [] #search_content를 위한 리스트
        for title, liked in sorted_items_by_value:
            print("=" * 60)
            print(f'{i + 1}.{title} 좋아요: {liked}')
            posts.append((title, filename_map[title]))
            i += 1
        
        return posts #search_content에 posts 정보를 보냄

    def search_content(keyword):
        print(f"🔎 == 내용에 '{keyword}'가 포함된 게시글 검색 결과 == 🔎")
        i = 0
        posts = []
        found = False
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read() # 파일 내용 전체를 읽음
                    if keyword in content:# 전체 내용에 키워드가 있는지 확인
                        # 키워드가 있다면, 제목을 찾아서 출력
                        file.seek(0) # 파일 포인터를 맨 앞으로 다시 옮기는 코드 제목을 뽑기 위함
                        for line in file:
                            if line.startswith('제목:'):
                                title = line.split(':', 1)[1].strip()
                                print("=" * 60)
                                print(f" -> '{i + 1}. {keyword}' |  게시글 제목: {title}")
                                posts.append((title, filename))
                                i += 1
                                found = True
                                break
            except Exception as e:
                print(f"❗️ 처리 중 오류 발생: {e}")

        if not found:
            print(f"'{keyword}'를 포함하는 게시글을 찾을 수 없습니다.")

        return posts
    
    def show_post_content(filename):  # 특정 게시글의 전체 내용을 보여주는 함수
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                print("=" * 60)
                print("게시글 전체 내용")
                print("=" * 60)
                print(file.read()) # 게시글 내용을 불러오기
                print("=" * 60)
        except FileNotFoundError:
            print("해당 파일을 찾을 수 없습니다.")
        except Exception as e:
            print(f"❗️ 파일을 읽는 중 오류가 발생했습니다: {e}")

    def select_and_view_post(posts):  # 게시글 목록을 불러오면 (전체글, 카테고리, 최신순 등등) 그 상태에서 번호를 입력해 글 내용을 불러오는 함수
        if not posts:
            print("표시할 게시글이 없습니다.")
            return
        try:
            choice = int(input("\n게시글 번호를 입력하세요 (0: 취소): "))
            if choice == 0:
                print("취소되었습니다.")
                return
            elif 1 <= choice <= len(posts):
                selected_title, selected_filename = posts[choice - 1]
                print(f"\n선택한 게시글: {selected_title}")
                BoardManager.show_post_content(selected_filename)
            else:
                print("잘못된 번호입니다.")
        except ValueError:
            print("숫자를 입력해주세요.")


def main():
    while True:
        print("\n" + "=" * 50)
        print("🔎 게시판 검색 시스템 🔎")
        print("=" * 50)
        print("1.📃 전체 게시글 보기")
        print("2.🏷️  카테고리별 검색")
        print("3.⏰ 최신순 정렬")
        print("4.👍 좋아요순 정렬")
        print("5.🔎 작성자, 내용 검색")
        print("0. 종료")
        print("=" * 50)
        
        try:
            choice = int(input("메뉴를 선택하세요: "))
            
            if choice == 0:
                print("프로그램을 종료합니다.")
                break
            elif choice == 1:
                posts = BoardManager.get_titles_from_post()
                BoardManager.select_and_view_post(posts)
            elif choice == 2:
                category = input("검색할 카테고리를 입력하세요: ")
                posts = BoardManager.Category_search_titles(category)
                BoardManager.select_and_view_post(posts)
            elif choice == 3:
                posts = BoardManager.Latest_post()
                BoardManager.select_and_view_post(posts)
            elif choice == 4:
                posts = BoardManager.Most_liked_post()
                BoardManager.select_and_view_post(posts)
            elif choice == 5:
                keyword = input("검색할 키워드를 입력하세요: ")
                posts = BoardManager.search_content(keyword)
                BoardManager.select_and_view_post(posts)
            else:
                print("잘못된 메뉴 번호입니다. 다시 선택해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break

if __name__ == "__main__":
    main()
