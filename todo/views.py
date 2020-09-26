from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import todos
from .forms import Todoform
from django.utils import timezone


# Create your views here.
def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        # create new user
        if request.POST['password1'] == request.POST['password2']:
           try: 
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('currenttodos')

           except IntegrityError:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error':'A User with that name already excist'})                    
        else:
              return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords dont match'})

@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':Todoform()})
    else:
       try: 
            form = Todoform(request.POST)
            newform = form.save(commit=False)
            newform.user = request.user
            newform.save()
            return redirect('currenttodos')
       except ValueError:
             return render(request, 'todo/createtodo.html', {'form':Todoform(), 'error':'Bad input try again.'})

@login_required
def viewtodo(request, todo_key):
    todo_detail = get_object_or_404(todos, pk=todo_key, user=request.user)
    if request.method == 'GET':
        form = Todoform(instance=todo_detail)
        return render(request, 'todo/viewtodo.html', {'todo': todo_detail, 'form': form})
    else:
        form = Todoform(request.POST, instance=todo_detail)
        form.save()
        return redirect('currenttodos')

@login_required
def completedtodos(request):
    todoss = todos.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todoss})

@login_required
def completed(request, todo_key):
      todo_detail = get_object_or_404(todos, pk=todo_key, user=request.user)
      todo_detail.datecompleted = timezone.now()
      todo_detail.save()
      return redirect('currenttodos')

@login_required
def deletetodo(request, todo_key):
      todo_detail = get_object_or_404(todos, pk=todo_key, user=request.user)
      todo_detail.delete()
      return redirect('currenttodos')

@login_required
def currenttodos(request):
    todoss = todos.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todoss})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('currenttodos')
        else:
            return render(request, 'todo/loginuser.html', {'error':'TRY AGAIN', 'form':AuthenticationForm()})