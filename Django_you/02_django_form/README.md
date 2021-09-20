# README

* Form은 Django 프로젝트의 주요 유효성 검사 도구들 중 하나이며, 공격 및 우연한 데이터 손상에 대한 중요한 방어수단
* Django는 위와 같은 form 기능의 방대한 부분을 단순화하고 자동화 할 수 있으며, 프로그래머가 직접 작성한 코드에서 수행할 수 있는 것보다 더 안전하게 수행할 수 있음
* Django 는 Form에 관련된 작업의 아래 세 부분을 처리해 줌
  1. 렌더링을 위한 데이터 준비 및 재구성
  2. 데이터에 대한 HTML forms 생성
  3. 클라이언트로부터 받은 데이터 수신 및 처리

#### ModelForm 선언하기

```django
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'my-title',
                'placeholder': 'Enter the title',
                'maxlength': 10,
            }
        )
    )
    content = forms.CharField(
        label='제목',
        widget=forms.Textarea(
            attrs={
                'class': 'my-content',
                'placeholder': 'Enter the content',
                'rows': 5,
                'cols': 50,
            }
        )
    )

    class Meta:
        model = Article
        fields = '__all__' 
```

#### Form 사용하기

```django
# articles/views.py 

@require_http_methods(['GET', 'POST'])
def create(request):
    # update
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid(): # 유효성 검사
            article = form.save()
            return redirect('articles:detail', article.pk)
    else: # 데코레이터가 없다면 포스트가 아닌 다른 모든 메서드가 들어가게 됨
    # new
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)
```

```django
# create.html

{% extends 'base.html' %}

{% block content %}
  <h1>CREATE</h1>
  <form action="{% url 'articles:create' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
  <hr>
  <a href="{% url 'articles:index' %}">[back]</a>
{% endblock  %}
```

#### Bootstrap 사용하기

```python
# forms.py

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'my-title',
                'placeholder': 'Enter the title',
                'maxlength': 10,
            }
        ),
        error_messages={
            'required': '내용 적으삼'
        }
    )
```

```html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
  <h1>CREATE</h1>
  <form action="{% url 'articles:create' %}" method="POST">
    {% csrf_token %}
    {% for field in form %}
      {% if field.errors %}
        {% for error in field.errors %}
          <div class="alert alert-warning" role="alert">{{ error|escape }}</div>
        {% endfor %}
      {% endif %}
      <div class="form-group">
        {{ field.label_tag }}
        {{ field }}
      </div>
    {% endfor %}
    <button class="btn btn-primary">작성</button>
  </form>
  <hr>
  <a href="{% url 'articles:index' %}">[back]</a>
{% endblock %}
```

```python
$ pip install django-bootstrap-v5
```

```python
# settings.py
INSTALLED_APPS = [
    'bootstrap5',
    ...
]
```

```html
# base.html

{% load bootstrap5 %}

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {% bootstrap_css %}
  <title>Document</title>
</head>
<body>
  <div class="container">
    {% block content %}
    {% endblock content %}
  </div>
  {% bootstrap_javascript %}
</body>
</html>
```

* 제목을 빈칸으로 제출하면 에러메세지 '내용 적으삼' 이 안뜸 ㅡㅡ 왜 안뜨지 ㅡㅡ

#### Handling HTTP requests

* Django에서 HTTP 요청을 처리하는 방법
  1. Django shortcut functions
  2. View decorators

* Django shortcuts functions

  * django.shortcuts 패키지는 개발에 도움 될 수 있는 여러 함수와 클래스를 제공
    * render()
    * redirect()
    * get_object_or_404()
    * get_list_or_404()

* Django View decorators

  * django는 다양한 HTTP 기능을 지원하기 위해 뷰에 적용할 수 있는 여러 데코레이터를 제공

    ```python
    from django.views.decorators.http import require_http_methods, require_POST, require_safe
    
    @require_safe # get 요청만 (조회)
    def index(request):
    	pass
    
    @require_http_methods(['GET', 'POST'])
    def create(request):
    	pass
    
    @require_safe # get 요청만 (조회)
    def detail(request, pk):
        pass
    
    @require_POST # post 요청만
    def delete(request, pk):
        pass
    
    @require_http_methods(['GET', 'POST'])
    def update(request, pk):
        pass
    ```

    