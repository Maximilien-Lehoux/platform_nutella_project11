from django.http import HttpResponse
from django.shortcuts import render
from .form import NameForm, FormLogin, ChangeInfosUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages


def login_page(request):
    """display of the login form and user login"""
    if request.method == 'POST':
        form = FormLogin(request.POST)
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "vous êtes connectés, vous pouvez "
                                      "enregistrer vos produits")
            return redirect('food:index')
        else:
            messages.error(request, "l'identifiant ou le mot de passe "
                                    "sont invalides")

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
            messages.success(request, "vous êtes enregistrés, "
                                      "vous pouvez-vous connecter")
            return redirect('accounts:login_page')

    else:
        form = NameForm()

    return render(request, 'accounts/register.html', {'form': form})


def connection_user(request):
    """association of the connection icon with the user's connection"""
    if not request.user.is_authenticated:
        return redirect('accounts:login_page')

    elif request.user.is_authenticated:
        current_user = request.user
        print(current_user.email)
        infos_user = User.objects.get(pk=current_user.pk)
        # form = ChangeInfosUser()

        if request.method == 'POST':
            form = ChangeInfosUser(request.POST)
            username = request.POST.get("username")
            email = request.POST.get("email")
            new_password = request.POST.get("password")
            new_password2 = request.POST.get("password2")

            if User.objects.filter(username=username).exists():
                messages.error(request, "l'identifiant existe")
                return redirect('accounts:connection_user')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "le mail existe")
                return redirect('accounts:connection_user')
            elif User.objects.filter(password=new_password).exists():
                messages.error(request, "le mot de passe existe")
                return redirect('accounts:connection_user')

            if form.is_valid() and username != "":
                current_user.username = username
                current_user.save()
                messages.success(request, "Votre nom d'utilisateur est modifié")

            if form.is_valid() and email != "":
                current_user.email = email
                current_user.save()
                messages.success(request,
                                 "Votre email est modifié")

            if form.is_valid() and new_password == new_password2 \
                    and new_password != "":
                modification = User.objects.get(username=current_user.username)
                modification.set_password(new_password)
                modification.save()
                messages.success(request,
                                 "Votre mot de passe est modifié")
                # return redirect("accounts:connection_user")
            return redirect("accounts:connection_user")
        else:
            form = ChangeInfosUser()

        context = {
            'infos_user': infos_user,
            'form': form
        }

        return render(request, 'accounts/my_account.html', context)


def disconnection_user(request):
    """association of the disconnection icon with the user's disconnection"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "vous êtes déconnectés")
        return redirect('food:index')
    else:
        messages.error(request, "Vous ne pouvez pas vous déconnecter "
                                "car vous n'êtes pas connectés")
        return redirect('accounts:login_page')


def change_infos_user(request):
    form = ChangeInfosUser()
    return render(request, 'accounts/my_account.html', {'form': form})
