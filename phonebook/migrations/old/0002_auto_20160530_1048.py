# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-30 03:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0001_squashed_0013_auto_20160505_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.CharField(default='КрасЭко', max_length=20, verbose_name='Компания'),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(default='Общий', max_length=20, verbose_name='Отдел'),
        ),
    ]
