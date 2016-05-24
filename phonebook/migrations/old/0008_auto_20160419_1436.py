# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0007_auto_20160419_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='extended',
        ),
        migrations.AddField(
            model_name='extendednumber',
            name='owner',
            field=models.ForeignKey(to='phonebook.User', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
    ]
