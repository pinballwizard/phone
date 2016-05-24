# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0004_auto_20160413_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=20, verbose_name='Фамилия', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mac_adress',
            field=models.CharField(max_length=12, verbose_name='MAC-адрес', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=10, verbose_name='Мобильный', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='number',
            field=models.CharField(max_length=5, verbose_name='Номер', unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='second_name',
            field=models.CharField(max_length=20, verbose_name='Отчество', blank=True),
        ),
    ]
