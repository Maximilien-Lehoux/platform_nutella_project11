from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='user name', max_length=100, required=False)
    email = forms.EmailField(label='email', max_length=100, required=False)
    password = forms.CharField(label='password', max_length=100, required=False)
    password2 = forms.CharField(label='re-write password', max_length=100, required=False)


class FormLogin(forms.Form):
    user_name = forms.CharField(label="Nom d'utilisateur", max_length=100)
    password = forms.CharField(label='Mot de passe', max_length=100)