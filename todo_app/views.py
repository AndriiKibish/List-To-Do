from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from todo_app.forms import TodoForm
from todo_app.models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo_app/home.html')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo_app/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo_app/login_user.html', {
                'form': AuthenticationForm(),
                'error': 'Username and password did not match'
            }
                          )
        else:
            login(request, user)
            return redirect('current_todo')


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo_app/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todo')

            except IntegrityError:
                return render(request, 'todo_app/signupuser.html', {
                    'form': UserCreationForm(),
                    'error': 'Such username already exists, try another one.',
                })

        else:
            return render(request, 'todo_app/signupuser.html', {
                'form': UserCreationForm(),
                'error': 'The passwords did not match',
            })


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo_app/create_todo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todo')
        except ValueError:
            return render(request, 'todo_app/create_todo.html', {
                'form': TodoForm(),
                'error': 'Wrong data passed in. Try again'
            }
                          )


@login_required
def current_todo(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'todo_app/current_todo.html', {'todos': todos})


@login_required
def completed_todo(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=False).order_by('completed')
    return render(request, 'todo_app/completed_todo.html', {'todos': todos})


@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    form = TodoForm(instance=todo)
    if request.method == 'GET':
        return render(request, 'todo_app/view_todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todo')
        except ValueError:
            return render(request, 'todo_app/view_todo.html', {'todo': todo, 'form': form, 'error': 'Bad info'})


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
        return redirect('current_todo')


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todo')
