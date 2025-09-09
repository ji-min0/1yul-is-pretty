# 3인 프로젝트 (프로젝트 최?) <<<<????????????



폴더명은 각각 blogcode, filteringcode, gamecode로 변경했습니다. 

---
### 파일을 못 읽는 오류 해결법 2가지
1) 'python -m 폴더.실행파일' 을 터미널에 직접 입력한다.
    <br>(예) python -m gamecode.main

2) blogcode, filteringcode, gamecode 각 폴더 안에 __init__.py 파일을 추가한다. 

=> 어떤 방법이 더 편한지 말씀해주시면 그걸로 반영할게요  
=> 최?: 된다면 어느 방법이든 상관 없는데 저는 __init__은 안되네요..  
=> 최?: CWD가 루트폴더인 상태에서 filter.py의 json파일 open 실행시 profanity.json이 인식이 안되는 문제가 있네요..  
 
---
###  blogcode/
- member1, 2, 3으로 폴더가 구분되어 있던 것을 blogcode라는 하나의 폴더에 병합시켰습니다.
- 이에 따라 코드에 일부 수정이 있었는데 확인 바랍니다. (경로를 하나하나 수정해서 빠뜨린 부분 있을 수도 있음)
    - folder_path = 'blogcode/posts' 로 변동
    - import 경로나 불러오는 함수의 별칭이 member1,2,3 이었어서 변경 완료함

### filteringcode/
- 최: 사용하지 않는 파일 정리 예정 아마 필터 파일만 사용하지 않을까 싶음.

### gamecode/
- 최: 게임 종료 선택지와 종료 선택시 블로그 메인 선택지로 돌아갈 수 있도록 만들 예정