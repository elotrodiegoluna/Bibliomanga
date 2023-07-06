from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import User, MangaUsuario, MangaTomo
from .validators import *

import os

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
    
class MangaUsuarioForm(forms.ModelForm):
    class Meta:
        model = MangaUsuario
        fields = ('nombre', 'desc', 'portada')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['portada'].widget.attrs.update({'class': 'form-control-file'})

    def clean_portada(self):
        portada = self.cleaned_data.get('portada')
        if portada:
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(portada.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError("La portada debe ser un archivo de imagen JPG, JPEG o PNG.")
        return portada
    

class MangaTomoForm(forms.ModelForm):
    archivo = forms.FileField(label='Archivo', required=True, widget=forms.ClearableFileInput(attrs={'accept': '.cbr,.cbz,.7z'}))

    class Meta:
        model = MangaTomo
        fields = ['tomo', 'desc', 'archivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'product-form'})
        self.fields['tomo'].required = True
        self.fields['desc'].required = True
        self.fields['archivo'].required = False

class EditarMangaForm(forms.ModelForm):
    class Meta:
        model = MangaUsuario
        fields = ['desc']