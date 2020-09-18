from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})
    else:
        # create new user
        if request.POST['password1'] == request.POST['password2']:
           try: 
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('currenttodos')

           except IntegrityError:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error':'A User with that name already excist'})                    
        else:
              return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': 'Passwords dont match'})

def currenttodos(request):
    return render(request, 'todo/currenttodos.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form':AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('currenttodos')
        else:
            return render(request, 'todo/login.html', {'error':'TRY AGAIN', 'form':AuthenticationForm()})