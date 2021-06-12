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


class UserAccount:
    def __init__(self):
        pass

    def change_infos(self, username, email, new_password, new_password2, request, form, current_user):
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
                return redirect("accounts:login_page")
