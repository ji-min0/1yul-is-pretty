# 지민 : 사용자 Log 기록 DB 생성

## dbconfig.py <- 파일 만들어야 합니다~~~

dbconfig = {
    'host': 'localhost',
    'user': 'root',
    'password': '--여기에 본인 비밀번호 입력--',
    'database': 'hanyul'
}


### accounts_setup.py
사용자 로그인 정보(id, password, is_admin 등)을 기록하는 accounts 테이블 자동 생성

### log_setup.py
사용자 이용 기록 정보(user_name, action, detail, timestamp)를 기록하는 user_logs 테이블 자동 생성

### comments_setup.py -> 이건 만들다 보니 건희님 파트라서 일단 두었습니다,,


## comment 필터링 기능이 없어서 추가했습니다.