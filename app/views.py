from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from app.models import CreatePassword
from .forms import CustomUserCreationForm, CreatePasswordForm
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required

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


@login_required
def editProfile(request, username):
    user = get_object_or_404(User, username=username)
    passwords = CreatePassword.objects.filter(username=username)
    data = {
        'form': CustomUserCreationForm(instance=user),
        'user': user
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST, instance=user)
        if formulario.is_valid():
            for p in passwords:
                p.username = user.username
                p.save()
            formulario.save()
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request, 'Perfil actualizado con éxito!')
            return redirect(to='view_passwords')
        data['form'] = formulario

    return render(request, 'app/boveda/user_profile.html', data)


@login_required
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


@login_required
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


def contactos(request):

    if request.method == 'POST':
        dir_email = request.POST['dir_email'] # Email que el usuario ingrese en el input.
        asunto = request.POST['asunto'] # Asunto del email.
        subject = request.POST['subject'] + ' Att: ' + dir_email # Mensaje del usuario.

        template = render_to_string('app/email_template.html', {'dir_name': dir_email, 'subject': subject})

        email = EmailMessage(
            asunto,
            template,
            settings.EMAIL_HOST_USER,
            ['junior31064049@gmail.com']
        )

        email.fail_silently = False
        try:
            email.send()
            messages.success(request, 'Tu Correo ha sido enviado con exito!.')
            return redirect(to='contactos')
        except:
            messages.error(request, 'Ha ocurrido un error al enviar el Email')

    return render(request, 'app/contactos.html')


@login_required
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


@login_required
def delete_password(request, id):
    password = get_object_or_404(CreatePassword, id=id)
    password.delete()
    messages.success(request, 'Contraseña eliminada correctamente!')
    return redirect(to='view_passwords')
