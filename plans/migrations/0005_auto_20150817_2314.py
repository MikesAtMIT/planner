# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0004_auto_20150817_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='order',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
