from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from catalog.models import Book, Author, BookInstance
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.http import HttpResponse
    
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.profile.id_number = form.cleaned_data.get('id_number')
        user.save()
        users = Group.objects.get(name='Users') 
        users.user_set.add(user)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(request=request, username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'register.html', {'form': form})

def registerManager(request):
    form = RegisterForm(request.POST)

    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Administrators').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.profile.id_number = form.cleaned_data.get('id_number')
        user.save()
        managers = Group.objects.get(name='Managers') 
        managers.user_set.add(user)
        return redirect('/')
    return render(request, 'register_manager.html', {'form': form})
    