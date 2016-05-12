from django.shortcuts import render, redirect
from django import forms
from sms.models import SMS
from django.http import HttpResponse


def sms_notice(request):
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
        str = "Получено смс от абонента {0} с текстом {1}".format(request.POST['SENDER'], request.POST['TEXT'])