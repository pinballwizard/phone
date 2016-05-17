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
    delivered = models.BooleanField('Доставлено', default=False)

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