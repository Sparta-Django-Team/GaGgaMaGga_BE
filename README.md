# B6팀(나이사)_가까?마까?(GaggaMagga) 프로젝트
<hr>

![ex_screenshot](./img/main.png)

<br>

## ****📌 프로젝트 개요****

  - Django Rest Framework과 Javascript를 활용하여 제주도의 맛집 추천 웹 서비스를 구축한다.
  - 유저 데이터를 기반으로 머신러닝 추천시스템을 활용하여 사용자 맞춤형 맛집을 추천해주고,
    사용자간 방문 후기를 서로 공유할 수 있는 플랫폼을 제공한다.
  - Timeline : 2022.07.07 ~ 2022.08.16
<br>

## ⚙ ****기능 명세서****

  - 사용자 환경(회원가입, 로그인, 회원정보 관리, 팔로우, 비활성화, 아이디/비밀번호 찾기)
  - 맛집 후기(리뷰) 작성/수정/삭제, 조회수 카운트, 좋아요, 검색 기능  
  - 후기 댓글 작성/수정/삭제
  - 후기 댓글의 대댓글 작성/수정/삭제 기능
  - 유저간 댓글, 후기의 좋아요 알림 기능
  - HTML/CSS/Javascript를 활용한 반응형 모바일 프론트엔드 페이지 구성

<br>

## 🔨 ****개발 포지션 구성****

  🛠**사재혁**
  - 유저 관리, 프로필, 개인설정 및 추가 기능
  - Docker, AWS 배포

  🛠**장진**
  - 머신러닝 장소 추천 기능, 후기 조회수, 페이지네이션

  🛠**나웅주**
  - 리뷰 조회 페이지, Best 리뷰 페이지 

  🛠**이지영**
  - 북마크 기능, 좋아요 기능, 댓글/대댓글 기능 

  🛠**이금빈**
  - 리뷰 생성 페이지, 팔로우 기능, 알림 기능, 검색 기능
  - Docker, AWS 배포

<br>

## ****⛓ Tech Stack****  

### Backend : <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/django rest framework-092E20?style=for-the-badge&logo=django&logoColor=white">
### Frontend : <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> 
### Server : <img src="https://img.shields.io/badge/AMAZON EC2-FFE900?style=for-the-badge&logo=amazon&logoColor=black"> <img src="https://img.shields.io/badge/DOCKER-3D97FF?style=for-the-badge&logo=docker&logoColor=white"> <img src="https://img.shields.io/badge/GUNICORN-2BB530?style=for-the-badge&logo=gunicorn&logoColor=white"> <img src="https://img.shields.io/badge/NGINX-2F9624?style=for-the-badge&logo=nginx&logoColor=white">
### Management : <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">

<br>

## 📚 ****Used Dataset****
  - 네이버 지도 v4 웹 크롤링을 통한 맛집 데이터 확보

<br>

## 🧱 ****Project Architecture****

![ex_screenshot](./img/architecture.png)

<br>

## 🕸 ****Wireframe****
![ex_screenshot](./img/wireframe.png)

<br>

## 🛢 ****Database ERD****
![ex_screenshot](./img/erd.png)

<br>

## 🎯 ****API****
### [USER API](https://www.notion.so/ea5288cd6b724843aba84b78b367cf2a)

![ex_screenshot](./img/user_api.png)

### [PLACE API](https://www.notion.so/77cdb6c85d724d59a46e38b6d4f307ee)

![ex_screenshot](./img/place_api.png)

### [REVIEW API](https://www.notion.so/6699ab1af4524a04ac4d44bad3294938)

![ex_screenshot](./img/review_api.png)

### [NOTIFICATION API](https://www.notion.so/783dbdb9d49d413ea8167fa98b5dc4ea)

![ex_screenshot](./img/notification_api.png)

<br>



## 🙏 ****Ground Rules****

- 하루에는 정해진 시간 안에 개발을 완료할 수 있도록 한다. (오전 9시 ~ 오후 10시)
- 깃 컨벤션을 지키고, 깃허브 프로젝트, 이슈 및 마일스톤을 활용하여 협업한다.
- 정기 회의체를 유지한다.(2회/일, 1차-10시, 2차-20시)

<br>

<hr>

### [Front-end Page](https://github.com/1TEAM12/GaGgaMaGga_FE)
### [Swagger API Docs](http://3.36.51.98/)
### [노션 진행 상황](https://www.notion.so/11-30-12-29-482dc47b71d44e968cf32283bb422238)
