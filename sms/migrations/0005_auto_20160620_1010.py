# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-20 03:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0004_smssended_delivered'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=20, verbose_name='Лицевой счет')),
                ('last_date', models.DateField(auto_now_add=True, verbose_name='Последняя дата обращения')),
            ],
            options={
                'verbose_name': 'Лицевой счет',
                'verbose_name_plural': 'Лицевой счет',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11, unique=True, verbose_name='Номер телефона')),
                ('blocked', models.BooleanField(default=False, verbose_name='Заблокирован')),
                ('ban_date', models.DateField(auto_now_add=True, verbose_name='Дата блокировки')),
            ],
            options={
                'verbose_name': 'Абонент',
                'verbose_name_plural': 'Абоненты',
            },
        ),
        migrations.AddField(
            model_name='smsreceived',
            name='response',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='sms.SmsSended', verbose_name='Ответная смс'),
        ),
        migrations.AddField(
            model_name='smssended',
            name='answer',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='sms.SmsReceived', verbose_name='Начальная смс'),
        ),
        migrations.AddField(
            model_name='account',
            name='subscriber',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sms.Subscriber', verbose_name='Абонент'),
        ),
    ]
