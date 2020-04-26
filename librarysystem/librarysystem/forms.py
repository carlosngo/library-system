from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    username = forms.CharField(max_length=30, help_text='Username')
    email = forms.EmailField(max_length=200, help_text='Email Address')
    id_number = forms.DecimalField(max_digits=15, decimal_places=0)

    class Meta:
        model = User
        fields = ('id_number', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2', )