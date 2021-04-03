from django.http import HttpResponse
from django.shortcuts import render
from .form import NameForm, FormLogin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


def login_page(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormLogin(request.POST)
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        # check whether it's valid
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('food:index')
        else:
            # Return an 'invalid login' error message.
            return HttpResponse('login invalid')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormLogin()

    return render(request, 'accounts/login.html', {'form': form})


# def register(request):
    # return render(request, 'accounts/register.html')


def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        name = request.POST.get("your_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        # check whether it's valid:
        if form.is_valid() and password == password2:
            User.objects.create_user(name, email, password)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'accounts/register.html', {'form': form})


def connection_user(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login_page')
    else:
        return redirect('food:index')


def disconnection_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('food:index')
    else:
        return redirect('accounts:login_page')