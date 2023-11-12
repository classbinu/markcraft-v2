# 마크 크래프트
몰입해서 익히는 마크다운 튜토리얼  
[https://markcraft.site](https://markcraft.site)

> 이 프로젝트는 [크래프톤 개발자 양성 프로그램 정글](https://jungle.krafton.com/)  
'week0. 3박 4일 미니 프로젝트' 과정 중 개발되었습니다.

## 기획 의도
마크다운(Markdown)은 일반 텍스트 기반의 경량 마크업 언어입니다.  
최근에는 마크다운을 사용하는 서비스가 늘어나고 있습니다.  
(옵시디언, 벨로그, 깃허브, 디스코드, 슬랙 등)  
  
하지만 많은 사람들이 마크다운을 배우는 것을 어려워합니다.  
그래서 저희 팀은 **마크다운을 쉽게 배울 수 있는** 서비스를 기획하였습니다.

## 주요 기능
1. 기본적인 마크다운 문법을 익힐 수 있는 강의실
2. 학습한 마크다운 문법으로 기록 갱졍을 할 수 있는 타임 어택
3. 자유롭게 마크다운을 사용할 수 있는 연습장

## 기술 스택
### 프론트 엔드
- CSS Framework: [TailwindCSS](https://tailwindcss.com/)
- Component Library: [Daisy UI](https://daisyui.com/)
- Templating Engine: [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)

### 백엔드
- Framework: [Flask](https://flask-docs-kr.readthedocs.io/ko/latest/index.html)

### 데이터베이스
- Nosql: [Mongodb](https://www.mongodb.com/ko-kr)

### 배포
- Server: [CloudType](https://cloudtype.io/)
- DB: [Mongodb Atlas](https://www.mongodb.com/ko-kr/cloud/atlas/lp/try4)

> 최초 배포 시에는 EC2 기반으로 배포하였으나,  
서버와 DB를 분리 및 프로젝트의 관리를 위해  
Paas기반으로 배포 환경을 변경하였습니다.

## 기술적 챌린지
### 1. marked.js의 코드 스니펫 미지원
- 코드 스니펫은 CSS를 이용해 별도 스타일 시트를 만들어 해결하였습니다.

### 2. TailwindCSS로 인한 기본 CSS 초기화
- marked.js 변환 후에 기본 스타일이 초기화되어 렌더링이 제대로 되지 않는 문제가 있었습니다.
- 마크다운 렌더링이 필요한 페이지에 h, ol, ul 등 기본 태그에 대한 스타일을 별도로 설정하였습니다.

### 3. 로그아웃 시 JWT 쿠키 미삭제 문제
- JWT를 쿠키에 저장했는데 로그아웃 시 쿠키가 삭제되지 않는 문제가 있었습니다.
- 이 문제의 원인은 서버에서 http 응답 시 httponly옵션이 True로 전송되어, 클라이언트단에서 자바스크립트로 쿠키 제어가 불가능해서 생긴 문제였습니다. httponly옵션을 False로 변경 후 정상적으로 쿠키 삭제가 되었습니다.
- 다만, 이 경우 자바스크립트로 쿠키 조작이 가능해 보안이 취약해 질 수 있습니다. 따라서 로그인 프로세스에 보안성을 강화에 대한 고민이 필요합니다.

## 개발 일정
2023/10/10 : 기획, 발표 자료 준비  
2023/10/11 : 로그인 관련 API, 페이지 CSS 구현  
2023/10/12 : 마크다운 렌더링 구현, 배포  
2023/10/13 : 최종 발표

## 역할 분배
**크래프톤 정글 3기 week0 101호 8팀**

[민상기](https://github.com/classbinu) UI, 프론트엔드 & 서버 연결, 발표  
[이세욱](https://github.com/o-ogie) 회원 기능 등 백엔드, EC2 및 DB 세팅  
[조윤희](https://github.com/y0c0y) 마크다운 렌더링 포함 프론트엔드 JS 주요 기능 구현

## 관련 포스팅
[[크래프톤 정글 3기] 마크크래프트 이전하기](https://velog.io/@classbinu/%ED%81%AC%EB%9E%98%ED%94%84%ED%86%A4-%EC%A0%95%EA%B8%80-3%EA%B8%B0-%EB%A7%88%ED%81%AC%ED%81%AC%EB%9E%98%ED%94%84%ED%8A%B8-%EC%9D%B4%EC%A0%84%ED%95%98%EA%B8%B0)

___
> 서비스에 대한 피드백, 질문은 언제든지 환영입니다.🥳  
classbinu@gmail.com