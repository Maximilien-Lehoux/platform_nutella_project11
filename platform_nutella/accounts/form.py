from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label="Nom d'utilisateur", max_length=100)
    email = forms.EmailField(label='email', max_length=100)
    password = forms.CharField(label='Mot de passe', max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmation', max_length=100)


class FormLogin(forms.Form):
    user_name = forms.CharField(label="Nom d'utilisateur", max_length=100)
    password = forms.CharField(label='Mot de passe', max_length=100)