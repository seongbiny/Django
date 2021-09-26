## 1. Signup

### signup

get방식과 post방식으로 나눠 받아야 한다 

```python
from django.views.decorators.http import require_http_method

if request.method == 'POST':
    pass
else:
    pass
```

GET방식의 요청이 "/accounts/signup/" 경로로 들어올 때 UserCreationForm을 활용하여 회원가입을 할 수 있도록 signup.html을 이용하여 페이지 구현

```python
from django.views.decorators.http import require_http_method
from django.contrib.auth.forms import UserCreationForm

@require_http_methods(['GET', 'POST'])
if request.method == 'POST':
    pass
else:
    form = UserCreationForm()
context = {
    'form': form,
}
return render(request, 'accounts/signup.html', context)
```

POST방식의 요청이 "/accounts/signup/" 경로로 들어올 때 **DB에 사용자의 정보를 저장**

1.유효성 검사

2.회원가입 후 "/accounts/login/" 경로로 리다이렉트

3.요청이 유효하지 않은 경우 입력 화면에 오류메세지 -> 알아서 잘 뜸

```python
from django.views.decorators.http import require_http_method
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

@require_http_methods(['GET', 'POST'])
if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid(): # 1.유효성 검사
    	user = form.save()
        auth_login(request, user)
        return redirect('accounts:login') # 2.리다이렉트
else:
    form = UserCreationForm()
context = {
    'form': form,
}
return render(request, 'accounts/signup.html', context)
```

### login

get방식과 post방식으로 나눠 받아야 한다 

```python
from django.views.decorators.http import require_http_method

if request.method == 'POST':
    pass
else:
    pass
```

GET방식의 요청이 "/accounts/login/" 경로로 들어올 때 로그인 할 수 있도록 login.html과 AuthenticationForm을 활용하여 구현

```python
from django.views.decorators.http import require_http_method
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login

if request.method == 'POST':
    pass
else:
    form = AuthenticationForm()
context = {
    'form': form,
}
return render(request, 'accounts/login.html', context)
```

POST방식의 요청이 "accounts/login/" 경로로 들어올 때  **로그인 정보를 세션에 저장**

1.AuthenticationForm 활용

2.유효성 검사

3.로그인 정상적 완료 index.html 반환

4.요청이 유효하지 않으면 화면에 오류메세지 출력

```python
from django.views.decorators.http import require_http_method
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login

if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        return render(request, 'accounts/index.html')
else:
    form = AuthenticationForm()
context = {
    'form': form,
}
return render(request, 'accounts/login.html', context)
```

