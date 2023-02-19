from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from todo_app.forms import TodoForm


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


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


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


def current_todo(request):
    return render(request, 'todo_app/current_todo.html')
