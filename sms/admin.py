from django.contrib import admin
from django.utils.html import format_html
from sms.models import SmsReceived, SmsSended, Subscriber, Account
from django.core.urlresolvers import reverse

@admin.register(SmsReceived)
class SmsReceivedAdmin(admin.ModelAdmin):
    def response_sms_link(self, obj):
        if obj.response:
            return format_html('<a href={0}>{1}</a>'.format(reverse('admin:sms_smssended_change', args=[obj.response.id]), obj.response.id))
        else:
            return obj.response
    date_hierarchy = 'date'
    list_select_related = ('response',)
    readonly_fields = ('date', 'smsid', 'agtid', 'inbox', 'sender', 'target', 'rescount', 'text', 'response', 'response_sms_link')
    list_display = ('date', 'smsid', 'agtid', 'inbox', 'sender', 'target', 'rescount', 'text', 'response_sms_link')
    search_fields = ['date', 'sender', 'target']
    list_filter = ('agtid',)


@admin.register(SmsSended)
class SmsSendedAdmin(admin.ModelAdmin):
    def answer_sms_link(self, obj):
        if obj.answer:
            return format_html('<a href={0}>{1}</a>'.format(reverse('admin:sms_smsreceived_change', args=[obj.answer.id]), obj.answer.id))
        else:
            return obj.answer
    date_hierarchy = 'date'
    list_select_related = ('answer',)
    readonly_fields = ('date', 'user', 'password', 'action', 'target', 'message', 'url', 'success', 'answer', 'answer_sms_link')
    list_display = ('date', 'action', 'target', 'message', 'success', 'answer_sms_link')
    search_fields = ['date', 'action', 'target']
    list_filter = ('action', 'success')


class ExtendedAccountAdmin(admin.TabularInline):
    model = Account
    extra = 0
    ordering = ['last_date']
    list_display = ('account', 'last_date')
    readonly_fields = ('account', 'last_date')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_date'
    readonly_fields = ('account', 'subscriber', 'last_date')
    list_display = ('account', 'subscriber', 'last_date')
    search_fields = ['account', 'subscriber', 'last_date']


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
    readonly_fields = ('mobile', 'create_date', 'last_date')
    list_display = ('mobile', 'create_date', 'last_date', 'blocked')
    search_fields = ['mobile']
    list_filter = ('blocked',)
    inlines = [ExtendedAccountAdmin]