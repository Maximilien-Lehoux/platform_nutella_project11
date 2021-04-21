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
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
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
                        send_mail(subject, email, 'admin@example.com',  # emai = 'AWS_verified_email_address'
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
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})
