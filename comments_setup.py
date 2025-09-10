from dbconfig import dbconfig
import mysql.connector
from mysql.connector import Error

def create_comments_table():
    try:
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS comments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            post_id INT NOT NULL,
            author_id VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            filtered TEXT NOT NULL,
            timestamp DATETIME NOT NULL
        ) CHARACTER SET utf8mb4;
        """
        cursor.execute(sql)
        conn.commit()
        print("✅ comments 테이블 생성 완료")
    except Error as e:
        print(f"⚠️ 테이블 생성 오류: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_comments_table()
