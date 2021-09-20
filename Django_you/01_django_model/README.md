# README

### Database API

* Django Shell
  * 일반 Python shell을 통해서는 장고 프로젝트 환경에 접근할 수 없음
  * 그래서 장고 프로젝트 설정이 load 된 Python shell을 활용해 DB API 구문 테스트 진행
* 기본 Django shell 보다 더 많은 기능을 제공하는 **shell_plus**를 사용해서 진행
  * Django-extensions 라이브러리의 기능 중 하나

```python
$ pip install ipython
$ pip install django-extensions
```

```django
# settings.py

INSTALLED_APPS = [
	...,
	'django_extensions',
	...,
]
```

```python
$ python manage.py shell_plus
```

#### CREATE

* 방법 1

  * ```shell
    article.title = 'first'
    article.content = 'django!'
    article.save()
    ```

* 방법 2

  * ```shell
    article = Article(title='second', content='django!!')
    article.save()
    ```

* 방법 3

  * ```shell
    Article.objects.create(title='third', content='django!!!')
    # save 자동으로 됨
    ```

앞으로 이 중 **방법 2**를 사용한다.

#### READ

* all()

  * ```shell
    Article.objects.all()
    ```

* get()

  * ```shell
    article = Article.objects.get(pk=1)
    Article.objects.get(content='django!')
    ```

* filter()

  * ```shell
    Article.objects.filter(content='django!')
    Article.objects.filter(title='first')
    ```

#### UPDATE

```shell
article = Article.objects.get(pk=1)
article.title = 'byebye'
article.save()
```

조회 한 후 변경하고 저장해야 수정이 된다.

#### DELETE

```shell
article = Article.objects.get(pk=1)
article.delete()
```





