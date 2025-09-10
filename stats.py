import datetime

# 로그 파일 이름 정의
log_file = "logs.txt"


def log_event(user_input: str, filtered_output: str) -> None: 
    """
    사용자 입력과 변환 결과를 logs.txt에 저장하는 함수
    """
    # 현재 시간 문자열 생성 (예: 2025-08-29 14:35:21)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a", encoding="utf-8") as f: 
        # 로그 포맷: [시간] 입력: ... -> 변환 결과: ...
        f.write(f"[{timestamp}] 입력: {user_input} -> 변환 결과: {filtered_output}\n")


