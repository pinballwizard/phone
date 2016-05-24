# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mac_adress',
            field=models.CharField(blank=True, max_length=12, verbose_name='mac-адрес'),
        ),
    ]
