from django import forms
from .models import CreationUser, CreatePassword
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError


class CreationUserForm(UserCreationForm):
    picture_profile = forms.ImageField(required=False)
    username = forms.TextInput()
    email = forms.EmailInput()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Contraseña (Confirmación)', widget=forms.PasswordInput)

    class Meta:
        model = CreationUser
        fields = ['picture_profile', 'first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        exclude = ['last_origin', 'is_superuser', 'is_staff', 'is_active', 'date_joined']


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
