from django.contrib import admin
from phonebook.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'number', 'mobile', 'mac_adress')
    search_fields = ['fullname','number','mobile']