from django.contrib import admin
from sms.models import SmsReceived, SmsSended, Subscriber


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
    readonly_fields = ('date', 'user', 'password', 'action', 'target', 'message', 'url', 'delivered')
    list_display = ('date', 'action', 'target', 'message', 'delivered')
    search_fields = ['date', 'action', 'target']
    list_filter = ('action', 'delivered')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    date_hierarchy = 'ban_date'
    readonly_fields = ('mobile', 'account', 'ban_date')
    list_display = ('mobile', 'account', 'ban_date', 'blocked')
    search_fields = ['mobile', 'account']
    list_filter = ('blocked',)