## 프레임워크 기반 웹 페이지 구현

각 단계별 구현 과정, 학습 내용 및 어려웠던 부분



### Django 시작하기

---------

**모든 프로젝트의 기본**

#### 1. 가상환경 설정

1)가상환경 만들기

pjt04(작업할 폴더)를 만들고 그 폴더 안에서 명령어를 친다.

`python -m venv venv(가상환경이름)`

`pjt04` 폴더 안에 `venv`이름의 하위폴더가 생성된다. 작업은 pjt04폴더 내에서 한다.

2)가상환경 활성화하기

pjt04폴더 안에서 `source venv/Scripts/activate`를 친다.

cmd 라인 바로 아래에 (venv)가 생기는데 활성화 되었다는 뜻이다.

3)가상환경 내에서 패키지 설치

* 설치된 패키지 목록 확인하기 : `pip list`

* 장고 패키지 설치 : `pip install django django_extensions`
  * sett
* 패키지 목록 관리 : `pip freeze > requirements.txt`
  * 다른 가상환경에서 이 패키지들을 설치하려면 : `pip install -r requirements.txt`

#### 2.

1)README파일과 gitignore파일 생성

`touch README.md .gitignore`

#### 3. git 버전관리

`git init` -> `git add .` -> `git commit -m 'first commit'` -> `git remote add origin ''`

---------

#### 4. django 진짜 시작

1.  project 생성 

   ```djan
   django-admin startproject pjt04 .
   ```

2.  서버 확인

   ```django
   python manage.py runserver
   ```

3.  언어, 시간 설정

   settings.py 에서 `LANGUAGE_CODE = 'ko-kr'` , `TIME_ZONE = 'Asia/Seoul'` 로 변경

4. application 생성

   ```django
   python manage.py startapp movies
   ```

   * app 생성 했으면 setting.py에 등록해줘야함

     settings.py 에서 `INSTALLED_APPS`에 `'movies',` 추가



