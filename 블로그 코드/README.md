<h1>
  Python Mini Blog Project<br>
  프로젝트 개요
</h1>
</h3>
Python Mini Blog는 파이썬 기본 기능만으로 구현한 콘솔 기반 미니 블로그/게시판 시스템입니다.<br>
사용자는 회원가입과 로그인을 통해 글을 작성하고, 작성한 글을 목록에서 확인할 수 있으며, 카테고리별 검색과 최신 글 순 정렬도 가능합니다.<br>
<br>
3인 팀 프로젝트로 설계되어, 각 팀원이 분업하여 기능을 구현했습니다.
</h3>
<br><br>

<!-- 기능 섹션 -->
<h2>기능</h2>

<h3>1. 회원 관리 (<code>member1.py</code>)</h3>
<ul>
  <li>회원가입, 로그인, 로그아웃 기능 제공</li>
  <li>로그인 여부에 따라 글 작성 가능</li>
  <li>관리자 권한 확인 가능</li>
  <li>사용자 정보는 JSON 파일(<code>users.json</code>)로 저장</li>
  <li><strong>주요 함수</strong>
    <ul>
      <li><code>register_user(username, password, is_admin=False)</code> : 회원가입</li>
      <li><code>login_user(username, password)</code> : 로그인</li>
      <li><code>logout_user()</code> : 로그아웃</li>
      <li><code>get_current_user()</code> : 현재 로그인 사용자 반환</li>
    </ul>
  </li>
</ul>

<h3>2. 게시글 작성 (<code>member3.py</code>)</h3>
<ul>
  <li>로그인한 사용자만 글 작성 가능</li>
  <li>제목, 내용, 카테고리 입력</li>
  <li>작성 시간과 작성자 정보 자동 저장</li>
  <li>글은 텍스트 파일로 저장 (<code>member2/test_posts/&lt;작성자&gt;_&lt;시간&gt;.txt</code>)</li>
  <li><strong>카테고리 선택</strong>
    <ol>
      <li>매우 좋음</li>
      <li>좋음</li>
      <li>그냥저냥</li>
      <li>나쁨</li>
      <li>매우 나쁨</li>
      <li>기타</li>
    </ol>
  </li>
</ul>

<h3>3. 게시글 조회 (<code>member2.py</code>)</h3>
<ul>
  <li>작성된 글 목록 출력</li>
  <li>각 글의 <strong>작성자</strong>, <strong>제목</strong>, <strong>작성 시간</strong> 표시</li>
  <li>카테고리별 검색 및 최신 글 정렬 지원</li>
  <li><strong>게시글 저장 형식</strong>
    <pre><code>작성자: 사용자ID
제목: 글제목
내용: 글내용
카테고리: 선택된카테고리
시간: 2025.09.01 10:30:00
</code></pre>
  </li>
</ul>

<h3>4. 메인 실행 (<code>main.py</code>)</h3>
<ul>
  <li>콘솔 기반 메뉴 제공
    <pre><code>1. 게시글 작성
2. 게시글 목록 보기
3. 회원 관리 (로그인/회원가입)
0. 종료
</code></pre>
  </li>
  <li>회원 관리 메뉴
    <pre><code>1. 회원가입
2. 로그인
3. 로그아웃
0. 메인으로 돌아가기
</code></pre>
  </li>
  <li>프로그램 종료 시 사용자 정보 자동 저장</li>
</ul>

<hr/>

<!-- 역할 섹션 -->
<h2>팀원 역할</h2>
<table>
  <thead>
    <tr>
      <th>팀원</th>
      <th>담당 기능</th>
      <th>주요 파일</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>김민주[팀장]</td>
      <td>회원 관리, 로그인 상태 관리, JSON 영속화, 작성자-게시글 연결</td>
      <td><code>main.py</code><code>member1.py</code></td>
    </tr>
    <tr>
      <td>김재진</td>
      <td>게시글 조회/정렬/카테고리 검색 기능 구현 (작성자/시간 표시)</td>
      <td><code>member2.py</code></td>
    </tr>
    <tr>
      <td>김민규</td>
      <td>게시글 작성 기능 구현 (로그인 사용자 연동, 카테고리 입력, 시간/작성자 저장)</td>
      <td><code>member3.py</code></td>
    </tr>
  </tbody>
</table>

<img width="3024" height="1964" alt="회원가입화면" src="https://github.com/user-attachments/assets/e71477b1-aafd-4f12-aec2-660e1571fd5b" />

<img width="3024" height="2500" alt="게시물 작성 및 검생" src="https://github.com/user-attachments/assets/a934cb26-4f73-4291-84f0-c09660002da8" />

<img width="1920" height="1200" alt="댓글" src="https://github.com/user-attachments/assets/20e9ab1d-1b00-4a83-b745-f58545a323c1" />

