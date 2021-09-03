from django.shortcuts import render, redirect # render함수는 html을 보내는역할
from .models import Movie
# Create your views here.

# C
## 사용자가 데이터를 제출할 빈 html을 제공
def new(request):
    return render(request, 'movies/new.html')

## 사용자가 제출한 데이터를 새로운 movies에 저장
def create(request):
    movie = Movie()
    movie.title = request.POST.get('title')
    movie.overview = request.POST.get('overview')
    movie.posterpath = request.POST.get('posterpath')
    movie.save()
    return redirect('movies:detail', movie.pk)

# R
## 전체 목록 조회
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

## 단일 상세 조회
def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)

# U
## 데이터를 제출한 기존 내용이 있는 html 제공
def edit(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/edit.html', context)

## 사용자가 제출한 데이터를 기존 movies에 수정 
def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.title = request.POST.get('title')
    movie.overview = request.POST.get('overview')
    movie.posterpath = request.POST.get('posterpath')
    movie.save()
    return redirect('movies:detail', movie.pk)

# D
## 기존 목록을 삭제
def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies:index')
    else:
        return redirect('movies:detail', movie.pk)