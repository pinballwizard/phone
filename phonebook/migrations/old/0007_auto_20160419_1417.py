# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0006_user_panel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedNumber',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Имя', blank=True, max_length=20)),
                ('number', models.CharField(verbose_name='Номер', blank=True, max_length=11)),
            ],
            options={
                'verbose_name_plural': 'Номер на панели',
                'verbose_name': 'Номер на панели',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(verbose_name='Мобильный', blank=True, max_length=11),
        ),
        migrations.AddField(
            model_name='user',
            name='extended',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='phonebook.ExtendedNumber'),
        ),
    ]
