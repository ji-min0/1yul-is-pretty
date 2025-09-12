import pandas as pd, pymysql
from dbconfig import dbconfig

class GameDataLoading:
    '''
    문제를 저장하거나 불러오는 class입니다.

    get_questions list를 가져갈 떄 현재는 데이터양이 적어 ORDER BY RAND() 하였습니다.
    추후 페이징 또는 데이터양이 많아진다면 랜덤순서를 별도로 저정할 필요가 있습니다. 
    '''
    def __init__(self, user_type:str = "0", file_path = None):
        self.user_type = user_type
        # CSV 파일의 열 이름과 데이터베이스 테이블의 열 이름을 일치시킵니다.
        self.columns = ["quiz_id","level","chapter","questions","choices","answers","explanations"]
        # --- CSV 파일 정보 ---
        self.file_path = './gamecode/feature/quiz_list_merge.csv' if file_path == None else file_path
    
    def connect_to_database(self):
        return pymysql.connect(
            host=dbconfig['host'],
            user=dbconfig['user'],
            password=dbconfig['password'],
            db=dbconfig['database'],
            charset=dbconfig['charset'],
            cursorclass=pymysql.cursors.DictCursor
        )

    def load_data_from_csv(self):
        """
        CSV 파일에서 데이터를 읽어와 pandas DataFrame으로 반환합니다.
        """
        try:
            # CSV 파일을 읽습니다. 한글 인코딩 문제 방지를 위해 'utf-8'을 사용합니다.
            df = pd.read_csv(self.file_path, encoding='utf-8')
            print(f"'{self.file_path}' 파일에서 {len(df)}개의 데이터를 성공적으로 읽었습니다.")
            return df
        except FileNotFoundError:
            print(f"오류: 파일 '{self.file_path}'을(를) 찾을 수 없습니다.")
            return None
        except Exception as e:
            print(f"CSV 파일 로드 중 오류가 발생했습니다: {e}")
            return None

    def insert_data_to_mysql(self, df):
        """
        DataFrame의 데이터를 MySQL 테이블에 삽입합니다.
        """
        if df is None or df.empty:
            print("삽입할 데이터가 없습니다.")
            return
        conn = self.connect_to_database()
        cursor = conn.cursor()
        # INSERT 쿼리문 생성
        # 예: INSERT INTO quiz_questions (level, chapter, questions, ...) VALUES (%s, %s, %s, ...)
        insert_columns = self.columns[1:]
        columns_str = ", ".join(insert_columns)
        values_str = ", ".join([f"%({col})s" for col in insert_columns])
        insert_query = f"INSERT INTO QUIZ_QUESTIONS ({columns_str}) VALUES ({values_str})"
        
        # DataFrame의 각 행을 딕셔너리 형태로 변환하여 리스트에 저장
        # to_dict('records')를 사용하면 각 행을 딕셔너리로 변환하여 리스트로 반환합니다.
        data_dicts = df[insert_columns].to_dict('records')

        try:
            # executemany를 사용하여 여러 행을 한 번에 삽입합니다.
            cursor.executemany(insert_query, data_dicts)
            conn.commit()
            print(f"총 {cursor.rowcount}개의 레코드를 'QUIZ_QUESTIONS' 테이블에 성공적으로 삽입했습니다.")
        except mysql.connector.Error as err:
            print(f"MySQL 삽입 중 오류가 발생했습니다: {err.msg}")
            conn.rollback() # 오류 발생 시 롤백
        finally:
            cursor.close()

    def set_data_csv_to_mysql(self, file_path:str = None):
        """
        QUIZ_QUESTIONS TABLE에 CSV 파일 정보를 INSERT 할 수 있습니다.
        file 위치 정보와 아래의 열을 가지고있어야합니다.
        "quiz_id","level","chapter","questions","choices","answers","explanations"
        """
        self.file_path = self.file_path if file_path == None else file_path

        df = self.load_data_from_csv()
        self.insert_data_to_mysql(df)

    def get_all_questions(self) -> list[dict]:
        """
        모든 문제를 출제합니다.
        """
        conn = None
        quiz_list = []
        try:
            conn = self.connect_to_database()
            with conn.cursor() as cursor:
                main_sql = "SELECT * FROM QUIZ_QUESTIONS ORDER BY RAND()"
                sql = f"SELECT CAST(@ROWNUM:=@ROWNUM+1 AS UNSIGNED) AS numbers, Q.* FROM ({main_sql}) Q, (SELECT @ROWNUM := 0) R"
                cursor.execute(sql)
                for row in cursor.fetchall():
                    quiz_list.append(row)
        except Exception as e:
            print(f"데이터베이스 연결/쿼리 오류: {e}")
        finally:
            # 열려있을때만 닫기
            if conn.open:
                conn.close()
        return quiz_list
        
    def get_chapter_questions(self) -> list[dict]:
        """
        요청된 단원의 문제를 출제합니다.
        """
        conn = None
        quiz_list = []
        select_chapter = self.user_type
        try:
            conn = self.connect_to_database()
            with conn.cursor() as cursor:
                main_sql = "SELECT * FROM QUIZ_QUESTIONS WHERE CHAPTER LIKE %s ORDER BY RAND()"
                sql = f"SELECT CAST(@ROWNUM:=@ROWNUM+1 AS UNSIGNED) AS numbers, Q.* FROM ({main_sql}) Q, (SELECT @ROWNUM := 0) R"
                cursor.execute(sql, f"{select_chapter}.%")
                for row in cursor.fetchall():
                    quiz_list.append(row)
        except Exception as e:
            print(f"데이터베이스 연결/쿼리 오류: {e}")
        finally:
            # 열려있을때만 닫기
            if conn.open:
                conn.close()
        return quiz_list
    
    def get_level_questions(self) -> list[dict]:
        """
        요청된 단원의 문제를 출제합니다.
        """
        conn = None
        quiz_list = []
        select_level = self.user_type
        try:
            conn = self.connect_to_database()
            with conn.cursor() as cursor:
                main_sql = "SELECT * FROM QUIZ_QUESTIONS WHERE LEVEL = %s ORDER BY RAND()"
                sql = f"SELECT CAST(@ROWNUM:=@ROWNUM+1 AS UNSIGNED) AS numbers, Q.* FROM ({main_sql}) Q, (SELECT @ROWNUM := 0) R"
                cursor.execute(sql, select_level)
                for row in cursor.fetchall():
                    quiz_list.append(row)
        except Exception as e:
            print(f"데이터베이스 연결/쿼리 오류: {e}")
        finally:
            # 열려있을때만 닫기
            if conn and conn.open: 
                conn.close()
        return quiz_list
        
    def get_setting_questions(self) -> dict[str, tuple]:
        """
        level과 chapter의 범위를 가져옵니다.
        """
        conn = None
        setting_dict = {}
        columns = ("level", "chapter")
        try:
            conn = self.connect_to_database()
            for column in columns:
                with conn.cursor() as cursor:
                    sql = f"SELECT DISTINCT {column} FROM QUIZ_QUESTIONS"
                    
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    # 리스트컴프리헨션 > tuple 변환합니다.
                    values = tuple([row[column] for row in rows])
                    
                    # 최종 딕셔너리에 키-값 쌍을 저장합니다.
                    setting_dict[column] = values
        except Exception as e:
            print(f"데이터베이스 연결/쿼리 오류: {e}")
        finally:
            # 열려있을때만 닫기
            if conn.open:
                conn.close()
        return setting_dict

if __name__ == "__main__":
    loader = GameDataLoading(1)
    # # csv to sql
    loader.set_data_csv_to_mysql()

#     # # select test
    # re = loader.get_all_questions()
    # print(re)