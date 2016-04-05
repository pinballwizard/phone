from django.contrib import admin
from phonebook.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['fullname','number','mobile']