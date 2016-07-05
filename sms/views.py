from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django import forms
from sms.models import SmsReceived, SmsSended, Subscriber, Account
from django.http import HttpResponse, Http404
import json
import datetime
import requests
import pymssql
import logging
import re

logger = logging.getLogger('sms')


def mssql_connect(client_id):
    state = False
    conn_data = {
        'server': 'ksql02.ksk.loc:1434',
        'user': 'rd',
        'password': 'L151?t%fr',
        'database': 'DataForSMS',
        # 'as_dict': True,
    }
    try:
        with pymssql.connect(**conn_data) as connection:
            with connection.cursor() as cursor:
                # query = 'SELECT AnswerText FROM DataTable WHERE AbonentId={0}'.format(id)
                query = 'SELECT Date1,Date2,Date3,Value1,Value2,Value3 FROM DataTable WHERE AbonentId={0}'.format(client_id)
                logger.info('Database query -> {0}'.format(query))
                try:
                    cursor.execute(query)
                    query_result = cursor.fetchone()
                    logger.warning('Database result -> {0}'.format(query_result))
                    if query_result:
                        query_zip = zip(query_result[0:3], query_result[3:6])
                        bad_time = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)
                        z = [item for item in query_zip if item[0] != bad_time]
                        result = ' | '.join(['{0} -> {1}'.format(item[0].date().strftime('%d.%m.%Y'), item[1]) for item in z])
                        state = True
                    else:
                        result = 'Показаний по номеру лицевого счета нет. Попробуйте позже.'
                except pymssql.OperationalError:
                    logger.error('Database error -> {0}'.format(pymssql.OperationalError))
                    result = 'Неверный номер лицевого счета. Обратитесь по номеру +73912286207'
                logger.info('Database result -> {0}'.format(result))
                return result, state
    except pymssql.DatabaseError:
        logger.error("Can't connect to database {0}".format(conn_data['server']))


class SmsSendForm(forms.Form):
    target = forms.CharField(max_length=12, required=True, label='')
    target.widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер'})
    text = forms.CharField(max_length=70, required=False, label='')
    text.widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите сообщение'})


def process_sms_text(sms_str):
    return re.search(r'(\d{10,19})', sms_str)


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
        logger.info('POST message Received -> {0}'.format(request.POST))
        sms = SmsReceived(
            smsid=request.POST['SMSID'],
            agtid=request.POST['AGTID'],
            inbox=request.POST['INBOX'],
            sender=request.POST['SENDER'],
            target=request.POST['TARGET'],
            rescount=request.POST['RESCOUNT'],
            text=request.POST['TEXT']
        )
        sms.save()
        client_id = process_sms_text(request.POST['TEXT'])
        if client_id:
            logger.info('In sms text -> {0} find id -> {1}'.format(request.POST['TEXT'], client_id.group(0)))
            text, state = mssql_connect(client_id.group(0))
        else:
            logger.info('In sms text -> {0} id not found'.format(request.POST['TEXT']))
            text = 'Не найден номер договора в смс.'
            state = False
        post_sms(text, sms, state, client_id)
    return HttpResponse(status=200)


def post_sms(message, received_sms, state, client_id):
    sms = SmsSended(
        user='1637111',
        password='1637111-123',
        action='post_sms',
        message=message,
        target=received_sms.sender,
        url='http://beeline.amega-inform.ru/sendsms/',
        answer=received_sms
    )
    sms.save()
    received_sms.response = sms
    received_sms.save()
    if state and client_id:
        s = Subscriber(
            mobile=received_sms.sender,
        )
        s.save()
        s.account_set.create(
            account=client_id,
        )
    status_code = send_sms(sms, state)
    return status_code


def send_sms(sms, state):
    logger.info('{3} to {0} with message {1} send to url {2}'.format(sms.target, sms.message, sms.url, sms.action))
    r = requests.post(sms.url, data=sms.data())
    if r.status_code is requests.codes.ok:
        sms.success = state
        sms.save()
    logger.info('SMS send status -> {0}'.format(r.status_code))
    return r.status_code


def test_sms(request):
    data = {
        'send_sms': SmsSendForm,
    }
    if request.method == 'POST':
        sms = SmsSended(
            user='1637111',
            password='1637111-123',
            action='post_sms',
            message=request.POST['text'],
            target=request.POST['target'],
            url='http://beeline.amega-inform.ru/sendsms/',
        )
        sms.save()
        if send_sms(sms=sms, state=True) is requests.codes.ok:
            return HttpResponse("Тестовая отправка на номер {0} прошла успешно".format(request.POST['target']))
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
    }
    return render(request, 'sms/smsstats.html', data)


def month_graph(request):
    if request.is_ajax():
        days_ago = datetime.date.today() - datetime.timedelta(days=365)

        sended_sms_filtred = SmsSended.objects.filter(date__date__gt=days_ago)
        sended_month_range = [dt for dt in sended_sms_filtred.datetimes('date', 'month')]
        sended_month_date = [dt.date().isoformat() for dt in sended_month_range]
        sended_count = [sended_sms_filtred.filter(date__month=month.month).count() for month in sended_month_range]

        received_sms_filtred = SmsReceived.objects.filter(date__date__gt=days_ago)
        received_month_range = [dt for dt in received_sms_filtred.datetimes('date', 'month')]
        received_month_date = [dt.date().isoformat() for dt in received_month_range]
        received_count = [received_sms_filtred.filter(date__month=month.month).count() for month in received_month_range]

        success_sms_filtred = SmsSended.objects.filter(date__date__gt=days_ago, success=True)
        success_month_range = [dt for dt in success_sms_filtred.datetimes('date', 'month')]
        success_month_date = [dt.date().isoformat() for dt in success_month_range]
        success_count = [success_sms_filtred.filter(date__month=month.month).count() for month in success_month_range]

        r = {
            'sended': list(zip(sended_month_date, sended_count)),
            'received': list(zip(received_month_date, received_count)),
            'success': list(zip(success_month_date, success_count))
        }
        return HttpResponse(json.dumps(r), 'application/javascript')
    else:
        raise Http404("Page for AJAX only")


def daily_graph(request):
    if request.is_ajax():
        days_ago = datetime.date.today()-datetime.timedelta(days=30)

        sended_sms_filtred = SmsSended.objects.filter(date__date__gt=days_ago)
        sended_day_range = [dt for dt in sended_sms_filtred.datetimes('date', 'day')]
        sended_day_date = [dt.date().isoformat() for dt in sended_day_range]
        sended_count = [sended_sms_filtred.filter(date__day=day.day).count() for day in sended_day_range]

        received_sms_filtred = SmsReceived.objects.filter(date__date__gt=days_ago)
        received_day_range = [dt for dt in received_sms_filtred.datetimes('date', 'day')]
        received_day_date = [dt.date().isoformat() for dt in received_day_range]
        received_count = [received_sms_filtred.filter(date__day=day.day).count() for day in received_day_range]

        success_sms_filtred = SmsSended.objects.filter(date__date__gt=days_ago, success=True)
        success_day_range = [dt for dt in success_sms_filtred.datetimes('date', 'day')]
        success_day_date = [dt.date().isoformat() for dt in success_day_range]
        success_count = [success_sms_filtred.filter(date__day=day.day).count() for day in success_day_range]

        r = {
            'sended': list(zip(sended_day_date, sended_count)),
            'received': list(zip(received_day_date, received_count)),
            'success': list(zip(success_day_date, success_count))
        }
        return HttpResponse(json.dumps(r), 'application/javascript')
    else:
        raise Http404("Page for AJAX only")