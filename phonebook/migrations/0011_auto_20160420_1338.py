# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0010_auto_20160420_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='second_name',
        ),
        migrations.AlterField(
            model_name='extendednumber',
            name='module',
            field=models.IntegerField(default=1, verbose_name='Модуль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=40, verbose_name='ФИО'),
        ),
    ]
