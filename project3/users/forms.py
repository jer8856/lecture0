from django import forms
from django.forms import ModelForm, CharField, TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    cellphone = forms.CharField(widget=TextInput(attrs={'type': 'number'}))

    class Meta:
        model = User
        fields = ['username', 'cellphone',  'password1', 'password2']
