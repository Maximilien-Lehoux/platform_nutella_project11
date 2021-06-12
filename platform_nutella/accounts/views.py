from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from .form import NameForm, FormLogin, ChangeInfosUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .manager import UserAccount


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
        infos_user = User.objects.get(pk=current_user.pk)
        # form = ChangeInfosUser()

        if request.method == 'POST':
            form = ChangeInfosUser(request.POST)
            username = request.POST.get("username")
            email = request.POST.get("email")
            new_password = request.POST.get("password")
            new_password2 = request.POST.get("password2")

            account_user = UserAccount()
            account_user.change_infos(username, email, new_password,
                                      new_password2, request, form,
                                      current_user)

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


def password_reset_request(request):
    """method that allows to obtain a new password when it is forgotten"""
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)

        account_user = UserAccount()
        account_user.forgot_password(request, password_reset_form)

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password_reset.html"
                  , context={"password_reset_form":password_reset_form})
