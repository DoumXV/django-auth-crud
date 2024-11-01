from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task

# Create your views here.


def home(request):
    return render(request, 'home.html')


def tasks(request):
    return render(request, 'tasks.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            "form": UserCreationForm
        })
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            # registrar usuario
            try:
                new_user = User.objects.create_user(
                    username=username, password=password1)
                new_user.save()
                login(request, new_user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })

        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden'
            })


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, "signin.html", {
            'form': AuthenticationForm
        })
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "signin.html", {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            print(user)
            login(request, user)
            return redirect('home')


def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    print(tasks)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })


def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            print(new_task)
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Porfavor ingrese datos validos'
            })
