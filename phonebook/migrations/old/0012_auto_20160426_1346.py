# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0011_auto_20160420_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendednumber',
            name='key',
            field=models.IntegerField(verbose_name='Кнопка'),
        ),
    ]
