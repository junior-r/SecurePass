from django import forms
from .models import CreatePassword
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreatePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=50)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Por seguridad ingrese su nombre de usuario, ej: john'}), min_length=3, max_length=100)

    def clean_username(self): # Valida si el usuario existe en la Base de Datos
        username = self.cleaned_data['username']
        exists = User.objects.filter(username=username).exists()
        if exists == True:
            return username
        else:
            raise ValidationError('Usuario Inválido')


    class Meta:
        model = CreatePassword
        fields = ['password', 'website', 'username']

