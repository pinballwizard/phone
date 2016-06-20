# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-16 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0006_auto_20160616_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.CharField(choices=[('kraseco', 'Красэко'), ('kic', 'КИЦ'), ('ministry', 'Министерство')], max_length=50, verbose_name='Компания'),
        ),
    ]
