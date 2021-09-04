# pjt04 README

### 1. models.py

Movie 라는 class를 만들고, 5개의 Field를 만들었다.

`title` : 제목 

`overview` : 줄거리

 `posterpath` : 포스터 사진 경로

 `created_at` : 작성한 시간

 `updated_at` : 수정한 시간

### 2. admin.py

```django
from django.contrib import admin
from .models import Movie # models 파일에서 Movie를 가져오겠다.

admin.site.register(Movie)
```

관리자 계정 등록

```python
$ python manage.py createsupteruser
```

### 3. pjt04/urls.py

```dja
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')) 
]
```

### 4. movies/urls.py

```django
app_name = 'movies' # namespace 작성
urlpatterns = [
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
```

### 5. views.py

각 페이지들의 동작 기능을 코드로 짠다.

### 6. movies/templates/movies

views.py 에서 화면에 나타나질 페이지가 필요한 4개의 html을 만든다.

`detail.html`, `edit.html`, `index.html`, `new.html`

### 7. templates/base.html

DRY => Don't Repeat Yourself

html들의 기본이 되는 base.html을 만든다.

기본 html 구조에서 bootstrap이 동작할 수 있게 코드를 추가하였고, nav bar 기능을 넣었다.

### 8. pjt04/settings.py

`TEMPLATES` 에서 디렉토리를 `BASE_DIR / 'templates'`로 설정한다.



#### 어려웠던 부분 & 느낀 점

* GET, POST 의 개념이 잘 와닿지않았다. 머리로는 이해가 가는데 코드를 짜면서 스스로 적용할 수 있을지 모르겠다. 
* 장고가 여러 파일들을 넘나들며 개발해야해서 순서가 많이 헷갈렸다. 그래서 리드미를 작성하면서 순서를 정확히 공부하고자 순서순으로 작성했다.
* html을 만들면서 기능 하나씩 추가하고 새로고침할때마다 바뀌는 모습을 보는게 가장 흥미로웠다. 가장 기본적인 기능을 넣기에도 시간이 부족해서 추가적으로 넣진 못했지만 만약 시간적 여유가 있었다면 더 본격적으로 제대로 꾸몄을 것 같다. 
* 관통프로젝트를 진행하면서 깨달은 것이 있다면 확실히 백엔드쪽 보다는 프론트엔드쪽에 내가 흥미있다는 것. 

