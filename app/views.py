from django.shortcuts import render, redirect
from django.contrib import messages

from app.models import CreatePassword
from .forms import CustomUserCreationForm, CreatePasswordForm
from django.contrib.auth import authenticate, login

# Create your views here.

def home(request):
    return render(request, 'app/index.html')


def registro(request):
    data = {
        'form': CustomUserCreationForm
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente!')

            return redirect(to='home')
        data['form'] = formulario

    return render(request, 'registration/registro.html', data)


def createPassword(request):
    data = {
        'form': CreatePasswordForm(),
    }
    if request.method == 'POST':
        formulario = CreatePasswordForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Contraseña Agregada con éxito')
            return redirect(to='view_passwords')
        data['form'] = formulario
    return render(request, 'app/boveda/create_password.html', data)


def view_passwords(request):
    passwords = CreatePassword.objects.all()
    data = {
        'passwords': passwords
    }
    return render(request, 'app/boveda/view_passwords.html', data)
