from django.contrib import admin
from sms.models import SMS
from django.contrib.admin.sites import AdminSite

AdminSite.site_header = 'Управление SMS рассылкой'
AdminSite.site_title = 'SMS рассылка'


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    list_display = ('smsid', 'agtid', 'inbox', 'sender', 'target', 'rescount', 'text')
    search_fields = ['sender','target']
    list_filter = ('agtid',)