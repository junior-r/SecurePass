from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from app.models import CreatePassword
from .forms import CustomUserCreationForm, CreatePasswordForm
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator

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


def profile(request, username):
    username = User.objects.get(username=username)
    return render(request, 'app/boveda/user_profile.html')


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
    page = request.GET.get('page', 1)
    try: 
        paginator = Paginator(passwords, 13)
        passwords = paginator.page(page)
    except:
        raise Http404
    data = {
        'entity': passwords,
        'paginator': paginator
    }
    return render(request, 'app/boveda/view_passwords.html', data)


def update_password(request, id):
    password = get_object_or_404(CreatePassword, id=id)
    data = {
        'form': CreatePasswordForm(instance=password)
    }

    if request.method == 'POST':
        formulario = CreatePasswordForm(data=request.POST, instance=password)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Contraseña actualizada con éxito!')
            return redirect(to='view_passwords')
        data['form'] = formulario
        

    return render(request, 'app/boveda/update_password.html', data)


def delete_password(request, id):
    password = get_object_or_404(CreatePassword, id=id)
    password.delete()
    messages.success(request, 'Contraseña eliminada correctamente!')
    return redirect(to='view_passwords')


def error_404(request, exception):
    return render(request, 'app/error_404.html')
