# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 05:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0012_auto_20160426_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendednumber',
            name='key',
            field=models.PositiveSmallIntegerField(verbose_name='Кнопка'),
        ),
        migrations.AlterField(
            model_name='extendednumber',
            name='module',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Модуль'),
        ),
    ]
