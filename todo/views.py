from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm, Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
def signup(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signup.html', {'form': UserCreationForm, 'error':'Username is not available'})
        else:
            return render(request, 'todo/signup.html', {'form': UserCreationForm, 'error':'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm})
    else:
       user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
       if user is None:
           return render(request, 'todo/login.html', {'form': AuthenticationForm, 'error':'username or password is invalid'})
       else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm })
    else:
        try:
            form    =   TodoForm(request.POST)
            newTodo =   form.save(commit=False)
            newTodo.user    =   request.user
            newTodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm,   'error': 'Invalid input'})
        
@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, completedate__isnull=True)
    return render(request, 'todo/currenttodo.html', {'todos': todos})
    
@login_required
def completetodos(request):
    todos = Todo.objects.filter(user=request.user, completedate__isnull=False).order_by('-completedate')
    return render(request, 'todo/completetodo.html', {'todos': todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)
    if request.method == 'GET':                
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form    =   TodoForm(request.POST, instance=todo) #trying to update existing todo
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Invalid input'})

def home(request):
    return render(request, 'todo/home.html')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completedate = timezone.now()
        todo.save()
        return redirect('currenttodos')
@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completedate = timezone.now()
        todo.delete()
        return redirect('currenttodos')