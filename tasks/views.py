from time import timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import TaskForm
from .models import Task
# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                form = UserCreationForm()
                return render(request, 'signup.html', {'form': form, "error": "Username already exists!"})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form, "error": "Passwords do not match."})




def tasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
        return render(request, 'tasks.html', {'tasks': tasks})
    else:
        return redirect('signin')


def task_detail(request, task_id):
    if request.user.is_authenticated and request.method == 'GET':
        task = Task.objects.get(id=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    elif request.user.is_authenticated and request.method == 'POST':
        task = Task.objects.get(id=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        else:
            return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        return redirect('signin')


def complete_task(request, task_id):
    if request.user.is_authenticated and request.method == 'POST':
        task = Task.objects.get(id=task_id, user=request.user)
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    else:
        return redirect('signin')


def tasks_completed(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
        return render(request, 'tasks_completed.html', {'tasks': tasks})
    else:
        return redirect('signin')


def delete_task(request, task_id):
    if request.user.is_authenticated and request.method == 'POST':
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
        return redirect('tasks')
    else:
        return redirect('signin')


def create_task(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'create_task.html', {'form': form})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            if form.is_valid():
                new_task.save()
                return redirect('tasks')
        except Exception as e:
            return render(request, 'create_task.html', {'form': form, 'error': str(e)})
        return render(request, 'create_task.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('tasks')