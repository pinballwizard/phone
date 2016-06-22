from django.db import models


class SmsReceived(models.Model):
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    smsid = models.CharField('ID сообщения', max_length=20)
    agtid = models.CharField('Номер конрагента', max_length=20)
    inbox = models.CharField('ID входящего ящика', max_length=20)
    sender = models.CharField('Номер отправителя', max_length=20)
    target = models.CharField('Номер получателя', max_length=20)
    rescount = models.SmallIntegerField('Количество')
    text = models.CharField('Текст сообщения', max_length=480)
    response = models.OneToOneField('SmsSended', on_delete=models.SET_DEFAULT, verbose_name='Ответная смс', default=None, null=True)

    class Meta:
        verbose_name = "Принятое SMS сообщение"
        verbose_name_plural = "Принятые SMS сообщения"

    def __str__(self):
        return "{0} -> {1}".format(self.sender, self.target)


class SmsSended(models.Model):
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    user = models.CharField('Пользователь', max_length=20)
    password = models.CharField('Пароль', max_length=20)
    action = models.CharField('Действие', max_length=20)
    target = models.CharField('Номер получателя', max_length=11)
    url = models.CharField('Адрес отправки', max_length=100)
    message = models.CharField('Текст сообщения', max_length=70)
    success = models.BooleanField('Успешно', default=False)
    answer = models.OneToOneField(SmsReceived, on_delete=models.SET_DEFAULT, verbose_name='Начальная смс', default=None, null=True)

    class Meta:
        verbose_name = "Отправленное SMS сообщение"
        verbose_name_plural = "Отправленные SMS сообщения"

    def data(self):
        return {
            'user': self.user,
            'pass': self.password,
            'action': self.action,
            'message': self.message,
            'target': self.target,
        }

    def __str__(self):
        return "{0} -> {1}".format(self.action, self.target)


class Subscriber(models.Model):
    mobile = models.CharField('Номер телефона', max_length=11, unique=True)
    blocked = models.BooleanField('Заблокирован', default=False)
    ban_date = models.DateField('Дата блокировки', auto_now_add=True)

    class Meta:
        verbose_name = "Абонент"
        verbose_name_plural = "Абоненты"

    def __str__(self):
        return self.mobile


class Account(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name="Абонент", default=None)
    account = models.CharField('Лицевой счет', max_length=20)
    last_date = models.DateField('Последняя дата обращения', auto_now_add=True)

    class Meta:
        verbose_name = "Лицевой счет"
        verbose_name_plural = "Лицевой счет"

    def __str__(self):
        return self.account