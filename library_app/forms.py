from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=False, label='Nome')
    last_name = forms.CharField(max_length=100, required=False, label='Apelido')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']