# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0006_auto_20150818_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='order',
            field=models.PositiveIntegerField(default=0, unique=True, blank=True),
        ),
    ]
