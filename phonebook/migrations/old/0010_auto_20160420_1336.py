# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0009_auto_20160419_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendednumber',
            name='key',
            field=models.IntegerField(unique=True, verbose_name='Кнопка', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extendednumber',
            name='module',
            field=models.IntegerField(verbose_name='Модуль', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='extendednumber',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='extendednumber',
            name='number',
            field=models.CharField(max_length=11, verbose_name='Номер'),
        ),
    ]
