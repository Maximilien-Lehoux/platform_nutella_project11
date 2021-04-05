from django.http import HttpResponse
from django.shortcuts import render
from .form import NameForm, FormLogin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


def login_page(request):
    """display of the login form and user login"""
    if request.method == 'POST':
        form = FormLogin(request.POST)
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('food:index')
        else:
            return HttpResponse('login invalid')

    else:
        form = FormLogin()

    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    """display of registration form and user registration"""
    if request.method == 'POST':
        form = NameForm(request.POST)
        name = request.POST.get("your_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        # check whether it's valid:
        if form.is_valid() and password == password2:
            User.objects.create_user(name, email, password)
            return redirect('accounts:login_page')

    else:
        form = NameForm()

    return render(request, 'accounts/register.html', {'form': form})


def connection_user(request):
    """association of the connection icon with the user's connection"""
    if not request.user.is_authenticated:
        return redirect('accounts:login_page')
    else:
        if request.user.is_authenticated:
            current_user = request.user
            print(current_user)
            infos_user = User.objects.get(pk=current_user.pk)
            context = {
                'infos_user': infos_user
            }

            return render(request, 'accounts/my_account.html', context)


def disconnection_user(request):
    """association of the disconnection icon with the user's disconnection"""
    if request.user.is_authenticated:
        logout(request)
        return redirect('food:index')
    else:
        return redirect('accounts:login_page')
