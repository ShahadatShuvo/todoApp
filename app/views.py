from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import TODOForm
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('priority')
        context = {
            'forms': form,
            'todos': todos,
        }
        return render(request, 'app/index.html', context)


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            'forms': form,
        }
        return render(request, 'app/login.html', context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {
                'forms': form,
            }
            return render(request, 'app/login.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            'forms': form,
        }
        return render(request, 'app/signup.html', context)
    else:
        form = UserCreationForm(request.POST)
        context = {
            'forms': form,
        }
        print(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'app/signup.html', context)


def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            print(form.cleaned_data)
            return redirect('home')
        else:
            context = {
                'forms': form,
            }
            return render(request, 'app/index.html', context)


def logout(request):
    logoutUser(request)
    return redirect('login')


def delete_todo(request, id):
    print(id)
    TODO.objects.get(pk=id).delete()
    return redirect(home)


def change_todo(request, id, status):
    todos = TODO.objects.get(pk=id)
    todos.status = status
    todos.save()
    return redirect('home')
