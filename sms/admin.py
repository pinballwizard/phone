from django.contrib import admin
from sms.models import SmsReceived, SmsSended
from django.contrib.admin.sites import AdminSite

AdminSite.site_header = 'Управление SMS рассылкой'
AdminSite.site_title = 'SMS рассылка'


@admin.register(SmsReceived)
class SmsReceivedAdmin(admin.ModelAdmin):
    list_display = ('date', 'smsid', 'agtid', 'inbox', 'sender', 'target', 'rescount', 'text')
    search_fields = ['date', 'sender', 'target']
    list_filter = ('agtid',)


@admin.register(SmsSended)
class SmsSendedAdmin(admin.ModelAdmin):
    list_display = ('date', 'action', 'target', 'message')
    search_fields = ['date', 'action', 'target']
    list_filter = ('action',)