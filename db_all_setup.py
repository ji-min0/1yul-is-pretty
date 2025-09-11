import mysql.connector
from mysql.connector import Error
from dbconfig import dbconfig

def create_database():
    try:
        # database 파라미터 제외하고 연결
        conn = mysql.connector.connect(
            host=dbconfig["host"],
            user=dbconfig["user"],
            password=dbconfig["password"]
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbconfig['database']} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;")
    except Error as e:
        print(f"⚠️ 데이터베이스 생성 오류: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

def create_accounts_table():
    try:
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            admin TINYINT(1) DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        cursor.execute(sql)
        conn.commit()
        print("✅ accounts 테이블 생성 완료")
    except Error as e:
        print(f"⚠️ accounts 테이블 생성 오류: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

def create_comments_table():
    try:
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        sql = """
        CREATE TABLE comments (
            comment_id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT NOT NULL,
            post_id INT NOT NULL,
            content_original TEXT NOT NULL,
            content_filtered TEXT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        cursor.execute(sql)
        conn.commit()
        print("✅ comments 테이블 생성 완료")
    except Error as e:
        print(f"⚠️ comments 테이블 생성 오류: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

def create_posts_table():
    try:
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            category ENUM('매우 좋음', '좋음', '그냥저냥', '나쁨', '매우 나쁨', '기타') DEFAULT '기타'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        cursor.execute(sql)
        conn.commit()
        print("✅ posts 테이블 생성 완료")
    except Error as e:
        print(f"⚠️ posts 테이블 생성 오류: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

def create_quiz_table():
    try:
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        sql = """
        CREATE TABLE quiz_questions (
            quiz_id INT AUTO_INCREMENT PRIMARY KEY,
            level TINYINT NOT NULL,
            chapter VARCHAR(20),
            questions varchar(255) NOT NULL,
            choices TEXT NOT NULL,
            answers CHAR(1) NOT NULL,
            explanations TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        cursor.execute(sql)
        conn.commit()
        print("✅ accounts 테이블 생성 완료")
    except Error as e:
        print(f"⚠️ accounts 테이블 생성 오류: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    create_database()
    create_accounts_table()
    create_comments_table()
    create_posts_table()
    create_quiz_table()