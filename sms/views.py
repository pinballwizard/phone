from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.db.models import Count
from sms.models import SmsReceived, SmsSended
from django.http import HttpResponse
import datetime
import requests
import pymssql


def mssql_connect(id):
    conn_data = {
        'server': "ksql02.ksk.loc:1434",
        'user': 'rd',
        'password': 'L151?t%fr',
        'database': 'DataForSMS',
    }
    with pymssql.connect(**conn_data) as connection:
        with connection.cursor() as cursor:
            query = "SELECT AnswerText FROM DataTable WHERE AbonentId={0}".format(id)
            try:
                cursor.execute(query)
                result = cursor.fetchone()[0]
            except:
                result = "Неверный номер договора. Обратитесь по номеру +73912286207"
    return result


class smsSendForm(forms.Form):
    target = forms.CharField(max_length=12, required=True, label='')
    target.widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Введите номер'})
    text = forms.CharField(max_length=70, required=False, label='')
    text.widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Введите сообщение'})


@csrf_exempt
def get_sms(request):
    """
    TEXT => текст сообщения
    INBOX => ID входящего ящика
    TARGET => номер получателя
    RESCOUNT => количество для тарификации
    SENDER => номер отправителя
    AGTID => номер конрагента
    SMSID => SMS ID
    LOGIN => Логин личного кабинет
    """
    if request.method == 'POST':
        sms = SmsReceived(
            smsid = request.POST['SMSID'],
            agtid = request.POST['AGTID'],
            inbox = request.POST['INBOX'],
            sender = request.POST['SENDER'],
            target = request.POST['TARGET'],
            rescount = request.POST['RESCOUNT'],
            text = request.POST['TEXT']
        )
        sms.save()
        text = mssql_connect(request.POST['TEXT'])
        post_sms(text, request.POST['SENDER'])
    return HttpResponse(status=200)


def post_sms(message, target):
    sms = SmsSended(
        user = '1637111',
        password = '1637111-123',
        action = 'post_sms',
        message = message,
        target = target,
        url = 'http://beeline.amega-inform.ru/sendsms/'
    )
    sms.save()
    print(sms.data())
    r = requests.post(sms.url, data=sms.data())
    if r.status_code is requests.codes.ok:
        sms.delivered = True
        sms.save()
    print(r.status_code)
    return r.status_code


def test_sms(request):
    data = {
        'send_sms': smsSendForm,
    }
    if request.method == 'POST':
        message = request.POST['text']
        target = request.POST['target']
        if post_sms(message, target) is requests.codes.ok:
            return HttpResponse("Тестовая отправка на номер {0} прошла успешно".format(target))
        else:
            return HttpResponse("Ошибка отправки")
    return render(request, 'sms/testsms.html', data)


def smsstats(request):
    last_month = datetime.datetime.now()-datetime.timedelta(days=30)
    data = {
        'sms_sended': SmsSended.objects.count(),
        'sms_recieved': SmsReceived.objects.count(),
        'sms_sended_last_month': SmsSended.objects.filter(date__date__gte=last_month).count(),
        'sms_recieved_last_month': SmsReceived.objects.filter(date__date__gte=last_month).count(),
        # 'sms_sended_avg_month': SmsSended.objects.filter(date__date__gte=last_month).count(),
        # 'sms_recieved_avg_month': SmsReceived.objects.filter(date__date__gte=last_month).count(),
        # 'most_active_users': SmsReceived.objects.aggregate(Count('sender'))
    }
    return render(request, 'sms/smsstats.html', data)