from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Music
from .forms import MusicForm

@require_safe
def index(request):
    musics = Music.objects.order_by('-pk')
    context = {
        'musics': musics,
    }
    return render(request, 'musics/index.html', context)

@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.save()
            return redirect('musics:detail', music.pk)
    else:
        form = MusicForm()
    context = {
        'form': form,
    }
    return render(request, 'musics/create.html', context)

@require_safe
def detail(request, pk):
    music = get_object_or_404(Music, pk=pk)
    context = {
        'music': music,
    }
    return render(request, 'musics/detail.html', context)

@require_POST
def delete(request, pk):
    music = get_object_or_404(Music, pk=pk)
    music.delete()
    return redirect('musics:index')

@require_http_methods(['GET', 'POST'])
def update(request, pk):
    music = get_object_or_404(Music, pk=pk)
    if request.method == 'POST':
        form = MusicForm(request.POST, instance=music)
        if form.is_valid():
            form.save()
            return redirect('musics:detail', music.pk)
    else:
        form = MusicForm(instance=music)
    context = {
        'music': music,
        'form': form,
    }
    return render(request, 'musics/update.html', context)