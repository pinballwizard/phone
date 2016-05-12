from django.db import models


class SMS(models.Model):
    ordid = models.CharField('ID сообщения', max_length=20)
    cnrid = models.CharField('Номер конрагента', max_length=20)
    sibnum = models.CharField('ID входящего ящика', max_length=20)
    sender = models.CharField('Номер отправителя', max_length=20)
    target = models.CharField('Номер получателя', max_length=20)
    rescount = models.SmallIntegerField('Количество')
    text = models.CharField('Текст сообщения', max_length=500)

    class Meta:
        verbose_name = "SMS сообщение"
        verbose_name_plural = "SMS сообщения"

    def __str__(self):
        return "{0} -> {1}".format(self.sender, self.target)