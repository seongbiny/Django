from django.shortcuts import render, redirect
from .forms import 
# Create your views here.
def index(request):
    todos = request.user.todo_set.all()
    context = {
        'todos': todos,
    }



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