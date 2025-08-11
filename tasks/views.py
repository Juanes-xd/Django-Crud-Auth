from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import TaskForm
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
    return render(request, 'tasks.html')

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