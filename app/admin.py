from django.contrib import admin
from .models import CreatePassword

# Register your models here.

class CreatePasswordAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'website', 'creation_date']
    search_fields = ['username', 'password', 'website', 'creation_date']
    list_filter = ['username', 'creation_date']
    list_per_page = 10


admin.site.register(CreatePassword, CreatePasswordAdmin)
