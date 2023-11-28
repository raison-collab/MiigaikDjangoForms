from django.forms import forms, CharField, TextInput, PasswordInput


class UserLoginForm(forms.Form):
    username = CharField(max_length=255, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = CharField(max_length=255, widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
