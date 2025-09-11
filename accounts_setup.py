import mysql.connector
from mysql.connector import Error
from dbconfig import dbconfig

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
        print(f"⚠️ 테이블 생성 오류: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_accounts_table()
