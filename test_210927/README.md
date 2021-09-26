1. project 생성 및 app 생성

```python
$ django-admin startproject crud .
$ python manage.py startapp articles
```

2. app 생성 후 settings.py 에 등록 + base.html 생성 후 등록

```python
# settings.py

INSTALLED_APPS = [
    'articles',
    ...
]

TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ..
    }
]
```

3. crud/urls.py 내용 추가

```python
from django.urls import path, include

urlpatterns = [
    path('articles/', include('articles.urls')),
]
```

4. models.py

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.CharField(max_length=500)

    def __str__(self):
        return self.title
    
$ python manage.py makemigrations
$ python manage.py migrate
```

5. articles/forms.py 생성 후 작성

```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'
```

6. **articles/admin.py 작성**

```python
from django.contrib import admin
from .models import Article

admin.site.register(Article)
```

```python
$ python manage.py createsuperuser
```

7. articles/urls.py -> views.py -> html

```python
from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
```

8. index 전체 목록 조회

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_method, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm

# 조회니까 GET 방식 요청
@require_safe
def index(request):
    # DB에 존재하는 모든 게시글의 목록을 표시
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)
```

9. create 새로운 게시글 작성 (GET, POST)

```python
@login_required
@require_http_method(['GET', 'POST'])
def create(request):
    if request.method == 'POST': # POST 방식 요청 들어올 때
        # ModelForm을 이용하여 요청과 함께 전송된 데이터를 검증
        form = ArticleForm(request.POST)
        # 데이터가 유효하면 DB에 저장
        if form.is_valid():
            article = form.save()
            # 상세 조회 페이지로 리다이렉트
            return redirect('articles:detail', article.pk)
    else: # GET 방식 요청 들어올 때
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/index.html', context)
```

10. detail 단일 게시글 상세 조회

```python
@require_safe
def detail(request, pk):
    # 표시할 게시글의 pk는 URL과 함께 전달된 게시글의 id
    article = get_object_or_404(Article, pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/dateil.html', context)
```

11. update 게시글 데이터 수정 

```python
@login_required
@require_http_method(['GET', 'POST'])
def update(request, pk):
    # 수정할 게시글의 pk는 URL과 함께 전달된 게시글의 id
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
       	form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article) # instance 주의
    context = {
        # 기존의 영화 데이터와 수정할 수 있는 form 표시
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)   
```

12. 게시글 데이터 삭제

```python
@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        article.delete()
    return redirect('articles/index.html')
```

13. signup 신규 사용자 생성

```python
@require_http_methods(['GET', 'POST'])
def signup(request):
    # 이미 인증되어 있는 사용자인지
    if request.user.is_authenticated:
        return redirect('accounts:index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # 데이터가 유효하다면
        if form.is_valid():
            # DB에 저장
            user = form.save()
            # 사용자를 로그인
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```

14. login 기존 사용자 인증

```python
@require_http_methods(['GET', 'POST'])
def login(request):
    # 인증되어있는 사용자는 index로 리다이렉트
    if request.user.is_authenticated:
        return redirect('aricles:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST) # 인자 2개
        if form.is_valid():
            # 유효하다면 로그인 form.get_user() 외우기
            auth_login(request, form.get_user())
            # 로그인 이전 페이지 url 인자 주의
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
```

14. logout 인증된 사용자 로그아웃

```python
@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('aritlces:index')
```

