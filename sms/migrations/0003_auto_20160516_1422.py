# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-16 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0002_auto_20160513_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsReceived',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('smsid', models.CharField(max_length=20, verbose_name='ID сообщения')),
                ('agtid', models.CharField(max_length=20, verbose_name='Номер конрагента')),
                ('inbox', models.CharField(max_length=20, verbose_name='ID входящего ящика')),
                ('sender', models.CharField(max_length=20, verbose_name='Номер отправителя')),
                ('target', models.CharField(max_length=20, verbose_name='Номер получателя')),
                ('rescount', models.SmallIntegerField(verbose_name='Количество')),
                ('text', models.CharField(max_length=480, verbose_name='Текст сообщения')),
            ],
            options={
                'verbose_name': 'Принятое SMS сообщение',
                'verbose_name_plural': 'Принятые SMS сообщения',
            },
        ),
        migrations.CreateModel(
            name='SmsSended',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.CharField(max_length=20, verbose_name='Пользователь')),
                ('password', models.CharField(max_length=20, verbose_name='Пароль')),
                ('action', models.CharField(max_length=20, verbose_name='Действие')),
                ('target', models.CharField(max_length=11, verbose_name='Номер получателя')),
                ('url', models.CharField(max_length=100, verbose_name='Адрес отправки')),
                ('message', models.CharField(max_length=70, verbose_name='Текст сообщения')),
            ],
            options={
                'verbose_name': 'Отправленное SMS сообщение',
                'verbose_name_plural': 'Отправленные SMS сообщения',
            },
        ),
        migrations.DeleteModel(
            name='SMS',
        ),
    ]
