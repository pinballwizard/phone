from django.contrib import admin
from phonebook.models import *
from django.contrib.admin.sites import AdminSite

AdminSite.site_header = 'Телефония КрасЭко'
AdminSite.site_title = 'Телефония КрасЭко'


@admin.register(ExtendedNumber)
class ExtendedNumberAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'owner')
    list_filter = ('owner',)
    ordering = ['key']


class ExtendedNumberInLine(admin.TabularInline):
    model = ExtendedNumber
    extra = 1
    ordering = ['key']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('number', 'last_name', 'mobile', 'mac_adress', 'panel')
    search_fields = ['fullname', 'number', 'mobile']
    list_filter = ('panel',)
    ordering = ['number']
    inlines = [ExtendedNumberInLine]
