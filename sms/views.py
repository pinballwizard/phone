from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django import forms
from sms.models import SMS
from django.http import HttpResponse
import requests
import pymssql


def mssql_connect():
    conn = pymssql.connect(
        server = "ksql02.ksk.loc:1434",
        user = 'rd',
        password = 'L151?t%fr',
        database = 'DataForSMS',
    )
    cursor = conn.cursor()
    cursor.execute('SELECT AnswerText FROM DataTable WHERE AbonentId=184015641911')
    return cursor.fetchone()


class smsSendForm(forms.Form):
    target = forms.CharField(max_length=12, required=True, label='')
    target.widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Введите номер'})
    text = forms.CharField(max_length=480, required=False, label='')
    text.widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Введите сообщение'})


@csrf_exempt
def get_sms(request):
    """
    ORDID = > ID сообщения
    CNRID = > номер конрагента
    SIBNUM = > ID входящего ящика
    SENDER = > номер отправителя
    TARGET = > номер получателя
    RESCOUNT = > количество для тарификации
    TEXT = > текст сообщения
    """
    if request.method == 'POST':
        print(request.POST)
        sms = SMS(
            ordid = request.POST['ORDID'],
            cnrid = request.POST['CNRID'],
            sibnum = request.POST['SIBNUM'],
            sender = request.POST['SENDER'],
            target = request.POST['TARGET'],
            rescount = request.POST['RESCOUNT'],
            text = request.POST['TEXT']
        )
        sms.save()
        # str = "Получено смс от абонента {0} с текстом {1}".format(request.POST['SENDER'], request.POST['TEXT'])
    return HttpResponse(status=200)


def test_con(request):
    s = mssql_connect()
    return HttpResponse(s)


def post_sms(message, target):
    con = {
        'user': '1637111',
        'pass': '1637111-123',
        'action': 'post_sms',
        'message': message,
        'target': target,
    }
    url = 'http://beeline.amega-inform.ru/sendsms/'
    r = requests.post(url, data=con)
    return True


def test_sms(request):
    data = {
        'send_sms': smsSendForm,
    }
    if request.method == 'POST':
        # message = request.POST['text']
        message = mssql_connect()
        target = request.POST['target']
        if post_sms(message, target):
            return HttpResponse("Тестовая отправка на номер {0} прошла успешно".format(target))
        else:
            return HttpResponse("Ошибка отправки")
    return render(request, 'phonebook/testsms.html', data)