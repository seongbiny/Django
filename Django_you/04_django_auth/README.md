# README

## Authentication System 1

### The Django Authentication System

* 필수 구성은 settings.py / INSTALLED_APPS 에 `django.contrib.auth`, `django.contrib.contenttypes`로 이미 구성됨

**Authentication (인증)**

* 신원 확인
* 사용자가 자신이 누구인지 확인하는 것

**Authorization (권한, 허가)**

* 권한 부여
* 인증된 사용자가 수행할 수 있는 작업을 결정

### 두번째 앱 (accounts) 생성하기

```python
$ python manage.py startapp accounts
```

* accounts로 지정하는 것을 권장

```python
# settings.py

INSTALLED_APPS = [
	...
	'accounts',
	...
]
```

```python
# crud/urls.py

urlpatterns = [
	path('accounts/', include('accounts.urls')),
]
```

```python
# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
	...
]
```

**app등록 및 url 설정!!**

### 로그인

* 로그인은 Session을 Create하는 로직과 같음
* Django는 우리가 session의 메커니즘에 생각하지 않게끔 도움
* 이를 위해 인증에 관한 built-in-forms를 제공

#### AuthenticationForm

* 사용자 로그인을 위한 form
* request를 첫번째 인자로 취함

#### login(request, user, backend=None)

* 현재 세션에 연결하려는 인증 된 사용자가 있는 경우 login() 함수가 필요
* 사용자를 로그인하며 view 함수에서 사용 됨
* HttpRequest 객체와 User 객체가 필요
* django의 session framework를 사용하여 세션에 user의 ID를 저장(==로그인)

```python
# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
	path('login/', views.login, name='login')
	...
]
```

```python
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET', 'POST'])
def login(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			auth_login(request, form.get_user())
			return redirect('articles:index')
	else:
		form = AuthenticationForm()
	context = {
		'form': form
	}
	return render(request, 'accounts/login.html', context)
```

```html
# accounts/login.html

{% extends 'base.html' %}

{% block content %}
  <h1>Login</h1>
  <form action="{% url 'accounts:login' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
{% endblock content %}
```

```html
# base.html

<body>
  <div class="container">
    <a href="{% url 'accounts:login' %}">Login</a>
    {% block content %}
    {% endblock content %}
  </div>
	...
</body>
```

### Authentication data in templates

**현재 로그인 되어있는 유저 정보 출력**

```html
# base.html

<body>
  <div class="container">
    <h3>Hello, {{ user }}</h3>
    <a href="{% url 'accounts:login' %}">Login</a>
    {% block content %}
    {% endblock content %}
  </div>
	...
</body>
```

### 로그아웃

* 로그아웃은 Session을 Delete하는 로직과 같음

#### logout(request)

* HttpRequest 객체를 인자로 받고 반환 값이 없음
* 사용자가 로그인하지 않은 경우 오류를 발생시키지 않음
* 현재 요청에 대한 session data를 DB에서 완전히 삭제하고, 클라이언트의 쿠키에서도 sessionid가 삭제됨
* 이는 다른 사람이 동일한 웹 브라우저를 사용하여 로그인하고, **이전 사용자의 세션 데이터에 액세스하는 것을 방지하기 위함**

```python
# accounts/urls.py

path('logout/', views.logout, name='logout'),
```

```python
# accounts/views.py

from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import logout as auth_logout

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('articles:index')
```

```html
# base.html

<body>
  <div class="container">
    <h3>Hello, {{ user }}</h3>
    <a href="{% url 'accounts:login' %}">Login</a>
    <form action="{% url 'accounts:logout' %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="Logout">
    </form>
    {% block content %}
    {% endblock content %}
  </div>
	...
</body>
```

### 로그인 사용자에 대한 접근 제한

#### Limiting access to logged-in users

* 로그인 사용자에 대한 엑세스 제한 2가지 방법
  1.  **is_authenticated** attribute
  2. **login_required** decorator

1번 방법 사용

```html
# base.html

<body>
  <div class="container">
    {% if request.user.is_authenticated %}
      <h3>Hello, {{ user }}</h3>
      <form action="{% url 'accounts:logout' %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="Logout">
      </form>
      </form>
    {% else %}
      <a href="{% url 'accounts:login' %}">Login</a>
    {% endif %}
    {% block content %}
    {% endblock content %}
  </div>
	...
</body>
```

```python
# accounts/views.py

# 인증된 사용자(로그인 상태)라면 로그인 로직을 수행할 수 없도록 처리
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
  
# 인증된 사용자(로그인 상태)만 로그아웃 로직을 수행할 수 있도록 처리
@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('aritcles:index')
```

```html
# articles/index.html

{% extends 'base.html' %}

{% block content %}
  <h1>Articles</h1>
  {% if request.user.is_authenticated %}
    <a href="{% url 'articles:create' %}">[CREATE]</a>
  {% else %}
    <a href="{% url 'accounts:login' %}">[새 글을 작성하려면 로그인하세요.]</a>
  {% endif %}
  <hr>
  ...
  {% endfor %}
{% endblock content %}
```

2번 방법 사용

```python
# articles/views.py

from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
	pass

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    pass
```

1. view 함수에 login_required 데코레이터 작성
2. 비로그인 상태에서 /accounts/create/ 경로로 요청 보내기
3. URL에 next 문자열 매개변수 확인

```python
# accounts/views.py

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
```

```html
# accounts/login.html

{% extends 'base.html' %}

{% block content %}
  <h1>Login</h1>
  <form action="" method="POST"> #next parameter 때문에 action 비워놈
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
{% endblock content %}
```

**문제점**

1. 비로그인 상태에서 게시글 삭제 시도(POST)
2. 로그인 검증
3. 로그인 페이지 응답(next='articles/1/delete/')
4. 로그인 요청(POST)
5. 로그인 성공 & next 경로로 리다이렉트 (GET)
6. 겟 요청으로 들어오는걸 데코레이터가 막기 때문에 405 Method Not Allowed 발생

```python
# aricles/views.py

@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        article.delete()
    return redirect('articles:index')
```

**login_required는 GET method request를 처리할 수 있는 view 함수에서만 사용해야 함**

## Authentication System 2

### 회원가입

#### UserCreationForm

* 주어진 username과 password로 권한이 없는 새 user를 생성하는 ModelForm
* 필드
  * username
  * password1
  * password2

```python
# accounts/urls.py

app_name = ' accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
```

```python
# accounts/views.py

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # 회원가입 후 자동으로 로그인 진행
            auth_login(request, user) # ''
            return redirect('articles:index')
       	else:
            form = UserCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/signup.html', context)
```

```html
# accounts/signup.html

{% extends 'base.html' %}

{% block content %}
  <h1>Signup</h1>
  <form action="{% url 'accounts:signup' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
{% endblock content %}
```

```html
# base.html

  <div class="container">
    {% if request.user.is_authenticated %}
      <h3>Hello, {{ user }}</h3>
      <form action="{% url 'accounts:logout' %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="Logout">
      </form>
    {% else %}
      <a href="{% url 'accounts:login' %}">Login</a>
      <a href="{% url 'accounts:signup' %}">Signup</a> #회원가입 링크
    {% endif %}
    {% block content %}
    {% endblock content %}
  </div>
```

### 회원탈퇴

* 회원탈퇴는 DB에서 사용자를 삭제하는 것과 같음

```python
# accounts/urls.py

app_name = 'accounts'
urlpatterns = [
    path('delete/', views.delete, name='delete'),
]
```

```python
# accoutns/views.py

from django.views.decorators.http import require_POST

@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete() # 순서! 탈퇴 후 -> 로그아웃 !!
        auth_logout(request) # 탈퇴하면서 해당 유저의 세션 데이터도 지움
    return redirect('articles:index')
```

### 회원정보 수정

#### UserChangeForm

* 사용자의 정보 및 권한을 변경하기 위해 admin 인터페이스에서 사용되는 ModelForm

```python
# accounts/urls.py

app_name = 'accounts'
urlpatterns = [
    path('update/', views.update, name='update'),
]
```

```python
# accounts/views.py

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        pass
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)
```

```html
# accounts/update.html

{% extends 'base.html' %}

{% block content %}
  <h1>회원정보수정</h1>
  <form action="{% url 'accounts:update' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
{% endblock content %}
```

```html
# base.html

    {% if request.user.is_authenticated %}
      <h3>Hello, {{ user }}</h3>
      <a href="{% url 'accounts:update' %}">회원정보수정</a>
      <form action="{% url 'accounts:logout' %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="Logout">
      </form>
      <form action="{% url 'accounts:delete' %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="회원탈퇴">
      </form>
    {% else %}
      <a href="{% url 'accounts:login' %}">Login</a>
      <a href="{% url 'accounts:signup' %}">Signup</a>
    {% endif %}
```

#### UserChangeForm 사용 시 문제점

* 일반 사용자가 접근해서는 안될 정보들까지 모두 수정이 가능해짐
* UserChangeForm을 상속받아 CustomUserChangeForm이라는 서브클래스를 작성해 접근 가능한 필드를 조정해야 함

#### CustomUserChangeForm 작성

```python
# accounts/forms.py 생성

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)
```

```python
# accounts/views.py

from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm

@login_required
@require_http_method(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
     else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)
```

### 비밀번호 변경

#### PasswordChangeForm

```python
# accounts/urls.py

app_name = 'accounts'
urlpatterns = [
    path('password/', views.change_password, name='change_password'),
]
```

```python
# accounts/views.py

form django.contrib.auth.forms import (
	AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)

@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)
```

**암호를 변경하면 로그인이 풀리고 메인화면으로 돌아간다 -> 세션변경이 되기때문**

#### 암호 변경 시 세션 무효화 방지

* update_session_auth_hash(request, user)
  * 비밀번호가 변경되면 기존 세션과의 회원 인증 정보가 일치하지 않게 되어 로그인 상태를 유지할 수 없다
  * 암호가 변경되어도 로그아웃되지 않도록 새로운 password hash로 session을 업데이트 함

```python
# accounts/views.py

from django.contrib.auth import update_session_auth_hash

@login_required
@require_http_method(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)
```



