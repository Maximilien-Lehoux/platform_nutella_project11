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

    def forgot_password(self, request, password_reset_form):
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "requête mot de passe"
                    email_template_name = "accounts/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    # 'domain': 'your-website-name.com',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',  # email = 'AWS_verified_email_address'
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'Un message contenant les '
                                              'instructions de '
                                              'réinitialisation du mot de '
                                              'passe a été envoyé dans votre '
                                              'boîte de réception.')
                    return redirect("food:index")
            messages.error(request, 'Un e-mail invalide a été saisi.')
