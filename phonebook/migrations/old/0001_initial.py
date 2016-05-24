# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('last_name', models.CharField(verbose_name='Фамилия', blank=True, max_length=20)),
                ('second_name', models.CharField(verbose_name='Фамилия', blank=True, max_length=20)),
                ('name', models.CharField(verbose_name='Имя', blank=True, max_length=20)),
                ('number', models.CharField(unique=True, verbose_name='Телефон', max_length=5)),
                ('mobile', models.CharField(verbose_name='Мобильный', blank=True, max_length=10)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
