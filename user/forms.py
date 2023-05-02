# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, PasswordInput


class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' , 'password']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 50%; margin-top: 5%',
            }),
            'password': PasswordInput(attrs={
                'class': '',
                'style': 'width: 50%; margin-top: 5%',
            }),
        }