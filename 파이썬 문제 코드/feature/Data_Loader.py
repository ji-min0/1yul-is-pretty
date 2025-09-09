# To do as a file loader: 
# 1. 파일 4개로 나눠서 가지고 오기 
# 2. 4지선다 콤마로 구분자 만들어서 보여주기(데이터 정리)

# pandas는 파이썬에서 가장 많이 쓰는 데이터 처리용 라이브러리(데이터 읽기, 정리, 분석 가능)
import pandas as pd, re
class GameDataLoading:

# 선택적으로 파일 경로 리스트를 받아옴 
# 4개 파일 경로를 사용함 
    def __init__(self, file_paths=None): 
        # 받은 파일 경로가 없으면 기본 네 개의 경로 사용
        self.file_paths = file_paths if file_paths else ['feature/questionfile1.csv', 'feature/questionfile2.csv', 'feature/questionfile3.csv', 'feature/questionfile4.csv']
        # 파일을 받아둘 빈 딕셔너리 
        self.data_files = {}
        # 인스턴스가 생성될 때 실행해서 모든 파일을 미리 읽어두는 기능
        self.load_files()

    #file_paths 리스트에 있는 모든 파일을 차례로 읽음 
    def load_files(self):
        for file in self.file_paths:
            try:
                # Pandas 데이터프레임 사용 
                data = pd.read_csv(file)
                # 공백이 있을 때를 대비해서 공백 삭제 
                # 칼럼명 오류에 대비
                data.columns = data.columns.str.strip()
                if 'levels' in data.columns:
                    data = data.rename(columns={'levels': 'level'})
                
                # 읽어들인 데이터를 파일명(key)과 쌍으로 data.failes 딕셔너리에 저장
                self.data_files[file] = data
            except FileNotFoundError:
                print(f"파일을 찾을 수 없습니다: {file}")
            except Exception as e:
                print(f"파일 로드 중 오류 발생: {file} - {str(e)}")
   
    def get_data(self, file_name):
        # 데이터 딕셔너리에 없으면 새로 읽기 시도 
        if file_name not in self.data_files:
            try:
                data = pd.read_csv(file_name, encoding='CP949') # DecodeError로 인한 설정 추가
                
                # 위와 동일한 방식으로 파일에 있을 빈칸이나 칼럼명 오류 해결
                data.columns = data.columns.str.strip()
                if 'levels' in data.columns:
                    data = data.rename(columns={'levels': 'level'})
                
                #file_name에 데이터 파일 저장
                self.data_files[file_name] = data
            except FileNotFoundError:
                print(f"파일을 찾을 수 없습니다: {file_name}")
                return None
            except Exception as e:
                print(f"파일 로드 중 오류 발생: {file_name} - {str(e)}")
                return None
        
        return self.data_files.get(file_name, None)

    def get_all_data(self):
        #데이터를 담을 리스트
        all_data = []

        for file in self.file_paths:
            #각 파일을 get_all_data 메서드를 사용해서 읽어옴 

            data = self.get_data(file)
            if data is not None:
            
                #파일 이름과, 파일에서 읽은 데이터를 딕셔너리 형태로 묶음
                file_dict = {
                    'file_name': file,
                    'data': data
                }

                #모든 파일에 대한 반복 후 모든 파일 정보가 담긴 리스트를 반환
                all_data.append(file_dict)
        
        return all_data
    
    def get_all_questions(self, unit_select:str="0"):
        # 모든 문제를 담을 빈 리스트
        all_questions = []

        # 특정 단원을 선택했으면
        if unit_select != "0":        

            # 첫 번째 파일 경로에서 숫자를 선택한 단원 번호로 바꿈 
            # re.sub은 파이썬의 re 모듈에 있는 sub() 함수를 사용한 문자열 치환 작업 
            # re.sub(pattern, repl, string) string에서 pattern에 해당하는 부분을 모두 replace
            # 파일 이름 내에서 숫자를 찾아서 주어진 단원 번호 문자열로 모두 대체하는 함수 
            file = re.sub('[0-9]', unit_select, self.file_paths[0])
            # 바뀐 파일 경로의 데이터 읽어오기 
            data = self.get_data(file)

            #데이터가 읽혔으면 다음을 진행. 
            if data is not None:

                #데이터를 각 행별 딕셔너리 리스트로 변환 
                questions = data.to_dict('records')
                
                # 각 문제 딕셔너리에 파일 이름을 추가해 파일 출처를 표시
                for question in questions:
                    question['file_name'] = file
                # 문제 리스트를 최종 리스트에 추가함
                all_questions.extend(questions)
            
            return all_questions 
        else: 
            # 단원별을 선택하지 않았으면 모든 파일 경로를 반복 
            for file in self.file_paths:
                data = self.get_data(file)
                if data is not None:
                    questions = data.to_dict('records')
                    for question in questions:
                        question['file_name'] = file
                    all_questions.extend(questions)
            
            return all_questions 

    def get_all_processed(self):
        #모든 파일을 데이터 리스트 형태로 가져옴. 
        all_data = self.get_all_data()
        #단원 선택 하지 않아도 전체 문제를 리스트 형태로 가져옴 
        all_questions = self.get_all_questions()
        
        #불러온 전체 데이터와 문제 리스트를 딕셔너리로 반환.
        return {
            'all_data': all_data,
            'all_questions': all_questions
        }


# loader = GameDataLoading()
# loader.load_files()
# result = loader.get_all_processed()
