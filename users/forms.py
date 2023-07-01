from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import User
from .validators import *

class CambiarAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='email', max_length=64)
    #password = forms.CharField(label='password', max_length=32)
    #username = forms.CharField(label='username', max_length=32)

    def __init__(self, *args, **kargs):
        super(RegistrationForm, self).__init__(*args, **kargs)

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")
        #fields = '__all__'

    #class Meta:
    #    model = User
    #    fields = ("email", "username", "password1", "password2")

class AuthForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")
    