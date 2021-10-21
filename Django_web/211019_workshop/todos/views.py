from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import Todo

# Create your views here.
def index(request):
    #todos = request.user.todo_set.all()
    todos = Todo.objects.order_by('-pk')
    context = {
        'todos': todos,
    }
    return render(request, 'todos/index.html', context)
    
@login_required
def new(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.save()
            return redirect('todos:index')
    else:
        form = TodoForm()
    context = {
        'form': form,
    }
    return render(request, 'todos/new.html', context)