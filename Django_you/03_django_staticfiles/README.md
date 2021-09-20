# README

### Static files

* 기본 경로

1. settings.py / INSTALLED_APPS 에 **django.contrib.staticfiles** 포함되어 있는지 확인

2. settings.py에서 **STATIC_URL** 을 정의

   ```python
   STATIC_URL = '/static/'
   ```

3. 템플릿에서 **static 템플릿 태그**를 사용하여 지정된 상대경로에 대한 URL을 빌드

   ```python
   {% load static %}
   <img src="{% static 'articles/sample-img-1.png' %}" alt="sample image">
   ```

4. 앱의 static 폴더에 정적 파일을 저장

   * articles/static/articles/sample-img-1.png

* 추가 경로

1. settings.py 에서 **STATICFILES_DIRS** 을 정의

   ```python
   STATICFILES_DIRS = [
       BASE_DIR / 'static',
   ]
   ```

   * articles/static/ 디렉토리 경로를 사용하는 것 외에 추가적인 정적 파일 경로 목록을 정의

---

#### 정적 파일 사용하기 - 기본 경로

articles/static/articles/sample-img-1.png

```html
# articles/detail.html

{% extends 'base.html' %}
{% load static %}

{% block content %}
  <img src="{% static 'articles/sample-img-1.png' %}" alt="sample image">
  <h2>DETAIL</h2>
  ...
{% endblock content %}
```

#### 정적 파일 사용하기 - 추가 경로

static/images/sample-img-2.png

```html
# base.html

{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
  ...
</head>
<body>
  <img src="{% static 'images/sample-img-2.jpg' %}" alt="sample image second">
  <div class="container">
    {% block content %}
    {% endblock content %}
  </div>
</body>
</html>
```

### Media file

> 사용자가 웹에서 업로드하는 정적 파일

```python
# settings.py

MEDIA_ROOT = BASE_DIR / 'media' # 사용자가 업로드 한 파일들을 보관할 디렉토리의 절대 경로

MEDIA_URL = '/media/' # MEDIA_ROOT에서 제공되는 미디어를 처리하는 URL, 업로드 된 파일의 주소(URL)를 만들어 주는 역할
```

```python
# crud/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 업로드 된 파일의 URL == settings.MEDIA_URL
# 위 URL을 통해 참조하는 파일의 실제 위치 == settings.MEDIA_ROOT
```

#### 이미지 업로드 (CREATE)

```python
# articles/models.py

class Article(models.Model):
	...
    # 실제 이미지가 저장되는 경로 지정 , 이미지 필드에 빈 값이 허용되도록 설정
    image = models.ImageField(upload_to='images/', blank=True) 
    ...
```

여기까지 하고

```python
$ pip install Pillow
$ python manage.py makemigrations
$ python manage.py migrate
$ pip freeze > requirements.txt
```

```html
# articles/create.html

<form action="{% url 'articles:create' %}" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="작성">
</form>
```

* enctype="multipart/form-data"
  * 파일/이미지 업로드 시에 반드시 사용해야 함 (전송되는 데이터의 형식을 지정)
  * <input type="file">을 사용할 경우에 사용

```python
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES) # 업로드 한 파일은 request.FILES 객체로 전달됨
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
	...
```

* 실제 파일 위치
  * MEDIA_ROOT/images/sample.png
* DB에 저장되는 것은 **파일의 경로**
  * images/sample.png

#### 이미지 업로드 (READ)

* article.image.url == 업로드 파일의 경로

* article.image == 업로드 파일의 파일 이름

  ```html
  # datail.html
  
  <img src="{{ article.image.url }}" alt="{{ article.image }}">
  ```

#### 이미지 업로드 (UPDATE)

```html
# update.html

{% block content %}
  <h1>UPDATE</h1>
  <form action="{% url 'articles:update' article.pk %}" method="POST">
    ...
{% endblock content %}
```

```python
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)
```

```html
# detail.html

{% extends 'base.html' %}
{% load static %}

{% block content %}
	...
  	<h2>DETAIL</h2>
  	<h3>{{ article.pk }} 번째 글</h3>
	{% if article.image %} # image가 없는 게시글의 경우 ~
    	<img src="{{ article.image.url }}" alt="{{ article.image }}">
  	{% endif %}
  	...
{% endblock content %}

```

#### 이미지 Resizing

1. **django-imagekit** 설치
2. INSTALLED_APPS 에 추가

```python
$ pip install django-imagekit
$ pip freeze > requirements.txt
```

* 원본 이미지를 재가공하여 저장 (원본x, 썸네일o)

```python
# models.py

from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

class Article(models.Model):
	...
    image = ProcessedImageField(
        blank=True,
        processors=[Thumbnail(200,300)],
        format='JPEG',
        options={'qulity': 90},
    )
    ...
```

```python
$ python manage.py makemigrations
$ python manage.py migrate
```

```html
# detail.html

<img src="{{ article.image_thumbnail.url }}" alt="{{ article.image_thumbnail }}">
```

