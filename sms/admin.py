from django.contrib import admin
from sms.models import SmsReceived, SmsSended


@admin.register(SmsReceived)
class SmsReceivedAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    readonly_fields = ('date', 'smsid', 'agtid', 'inbox', 'sender', 'target', 'rescount', 'text')
    list_display = ('date', 'smsid', 'agtid', 'inbox', 'sender', 'target', 'rescount', 'text')
    search_fields = ['date', 'sender', 'target']
    list_filter = ('agtid',)


@admin.register(SmsSended)
class SmsSendedAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    readonly_fields = ('date', 'user', 'password', 'action', 'target', 'message', 'url')
    list_display = ('date', 'action', 'target', 'message')
    search_fields = ['date', 'action', 'target']
    list_filter = ('action',)