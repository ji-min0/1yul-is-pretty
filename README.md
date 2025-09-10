# 3인 프로젝트 (프로젝트 최?)



폴더명은 각각 blogcode, filteringcode, gamecode로 변경했습니다. 

---
### 파일을 못 읽는 오류 해결법 2가지
1) 'python -m 폴더.실행파일' 을 터미널에 직접 입력한다.
    <br>(예) python -m gamecode.main

2) blogcode, filteringcode, gamecode 각 폴더 안에 __init__.py 파일을 추가한다. 

=> 어떤 방법이 더 편한지 말씀해주시면 그걸로 반영할게요

---
###  blogcode/
- member1, 2, 3으로 폴더가 구분되어 있던 것을 blogcode라는 하나의 폴더에 병합시켰습니다.
- 이에 따라 코드에 일부 수정이 있었는데 확인 바랍니다. (경로를 하나하나 수정해서 빠뜨린 부분 있을 수도 있음)
    - folder_path = 'blogcode/posts' 로 변동
    - import 경로나 불러오는 함수의 별칭이 member1,2,3 이었어서 변경 완료함

### filteringcode/
- 큰 변동은 없습니다. 폴더명 변경에 따른 코드 수정 (1건)

### gamecode/
- 폴더명 변경에 따라 csv 불러오는 경로를 변동했습니다. 