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
        CREATE TABLE IF NOT EXISTS comments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
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

if __name__ == "__main__":
    create_database()
    create_accounts_table()
    create_comments_table()