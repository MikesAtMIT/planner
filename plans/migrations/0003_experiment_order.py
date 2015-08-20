# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0002_auto_20150806_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
