import pymysql
from datetime import datetime

# DB 연결!
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='dain8154',
    db='hanyul',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# ==============================
# 카테고리 검색
# ==============================
def Category_search_titles(Category):
    print(f'🏷️ ==카테고리가 {Category}인 게시글 목록== 🏷️')
    with conn.cursor() as cur:
        sql = """SELECT id, name, title, content, created_at, category FROM posts"""
        cur.execute(sql)
        datas = cur.fetchall()

    found = False
    for data in datas:
        if Category == data['category']:
            print("=" * 60)
            print(f"{data['id']}. 제목: {data['title']}\n"
                  f"내용: {data['content']}\n"
                  f"시간: {data['created_at'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                  f"작성자: {data['name']}")
            found = True

    if not found:
        print("❗ 해당 카테고리에 속하는 게시글이 없습니다.")

# ==============================
# 최신순 정렬
# ==============================
def Latest_post():
    print('⏰ ==게시글 최신순으로 정렬== ⏰')
    with conn.cursor() as cur:
        sql = """SELECT id, name, title, content, created_at, category 
                 FROM posts ORDER BY created_at DESC"""
        cur.execute(sql)
        datas = cur.fetchall()

    for data in datas:
        print("=" * 60)
        print(f"시간: {data['created_at'].strftime('%Y-%m-%d %H:%M:%S')}, "
              f"제목: {data['title']}, 작성자: {data['name']}")

# ==============================
# 내용 검색
# ==============================
def search_content(keyword):
    print(f"🔎 == 내용에 '{keyword}'가 포함된 게시글 검색 결과 == 🔎")
    with conn.cursor() as cur:
        sql = """SELECT id, name, title, content, created_at, category FROM posts"""
        cur.execute(sql)
        datas = cur.fetchall()

    found = False
    results = []
    for data in datas:
        if keyword in data['content']:
            print("=" * 60)
            print(f"{data['id']}. 제목: {data['title']}\n"
                  f"시간: {data['created_at'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                  f"작성자: {data['name']}")
            found = True
            results.append(data)

    if not found:
        print(f"'{keyword}'를 포함하는 게시글을 찾을 수 없습니다.")

    return results

# ==============================
# 게시글 상세 보기
# ==============================
def show_post_content(post_id):
    with conn.cursor() as cur:
        sql = """SELECT id, name, title, content, created_at, category
                 FROM posts
                 WHERE id = %s"""
        cur.execute(sql, (post_id,))
        post = cur.fetchone()

    if post:
        print("=" * 60)
        print("게시글 전체 내용")
        print("=" * 60)
        print(f"제목: {post['title']}")
        print(f"작성자: {post['name']}")
        print(f"시간: {post['created_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"카테고리: {post['category']}")
        print("=" * 60)
        print(post['content'])
        print("=" * 60)
    else:
        print("❗ 해당 게시글을 찾을 수 없습니다.")

# ==============================
# 게시글 선택 후 상세 보기
# ==============================
def select_and_view_post(datas):
    if not datas:
        print("표시할 게시글이 없습니다.")
        return

    try:
        choice = int(input("\n게시글 번호를 입력하세요 (0: 취소): "))
        if choice == 0:
            print("취소되었습니다.")
            return
        elif 1 <= choice <= len(datas):
            selected = datas[choice - 1]
            selected_title = selected['title']
            selected_id = selected['id']
            print(f"\n선택한 게시글: {selected_title}")
            show_post_content(selected_id)
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

# ==============================
# 실행 예시
# ==============================
posts = search_content('1')   # 키워드 포함된 게시글 목록 출력
select_and_view_post(posts)   # 목록에서 번호 선택 → 상세 보기