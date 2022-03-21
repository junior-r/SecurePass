from django.urls import path
from .views import home, registro, createPassword, view_passwords

urlpatterns = [
    path('', home, name='home'),
    path('registro/', registro, name='registro'),
    path('create_password/', createPassword, name='create_password'),
    path('view_passwords/', view_passwords, name='view_passwords'),
]
