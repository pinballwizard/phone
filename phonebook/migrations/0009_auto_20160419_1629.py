# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0008_auto_20160419_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extendednumber',
            options={'verbose_name_plural': 'Номера на панели', 'verbose_name': 'Номер на панели'},
        ),
        migrations.AlterField(
            model_name='extendednumber',
            name='owner',
            field=models.ForeignKey(verbose_name='Просматривает', to='phonebook.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=40, blank=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='panel',
            field=models.BooleanField(default=False, verbose_name='Панель расширения'),
        ),
    ]
