from django.contrib import admin
from django.utils.html import format_html
from sms.models import SmsReceived, SmsSended, Subscriber
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
    readonly_fields = ('date', 'user', 'password', 'action', 'target', 'message', 'url', 'delivered', 'answer', 'answer_sms_link')
    list_display = ('date', 'action', 'target', 'message', 'delivered', 'answer_sms_link')
    search_fields = ['date', 'action', 'target']
    list_filter = ('action', 'delivered')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    date_hierarchy = 'ban_date'
    readonly_fields = ('mobile', 'account', 'ban_date')
    list_display = ('mobile', 'account', 'ban_date', 'blocked')
    search_fields = ['mobile', 'account']
    list_filter = ('blocked',)