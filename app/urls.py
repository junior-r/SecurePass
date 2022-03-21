from django.urls import path
from .views import home, registro, createPassword, view_passwords, update_password, delete_password

urlpatterns = [
    path('', home, name='home'),
    path('registro/', registro, name='registro'),
    path('create_password/', createPassword, name='create_password'),
    path('view_passwords/', view_passwords, name='view_passwords'),
    path('update_password/<id>/', update_password, name='update_password'),
    path('delete_password/<id>/', delete_password, name='delete_password'),
]
