
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Community
from .forms import CommunityForm

# Create your views here.

@require_safe
def index(request):
    community = Community.objects.order_by('-pk')
    
    context = {
        'community': community,
    }
    return render(request, 'community/index.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save()
            return redirect('community:detail', community.pk)
    else:
        form = CommunityForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


@require_safe
def detail(request, pk):
    movie = get_object_or_404(Community, pk=pk)
    context = {
        'movie': movie,
    }
    return render(request, 'community/detail.html', context)


@require_POST
def delete(request, pk):
    community = get_object_or_404(Community, pk=pk)
    community.delete()
    return redirect('community:index')

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    movie = get_object_or_404(Community, pk=pk)
    if request.method == 'POST':
        form = CommunityForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('community:detail', movie.pk)
    else:
        form = CommunityForm(instance=movie)
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'community/update.html', context)
