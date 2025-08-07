from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
                return HttpResponse("Username already exists!")
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],
                                                    password=request.POST['password1'])
                user.save()
                return HttpResponse(f"User {user.username} created successfully!")
        return HttpResponse("Passwords do not match!")
   