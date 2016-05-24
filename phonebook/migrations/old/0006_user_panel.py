# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0005_auto_20160413_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='panel',
            field=models.BooleanField(default=False, verbose_name='Панель расширение'),
        ),
    ]
