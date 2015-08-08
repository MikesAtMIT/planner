# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='objective',
        ),
        migrations.AlterField(
            model_name='experiment',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='status',
            field=models.CharField(default=b'O', max_length=1, choices=[(b'C', b'Completed'), (b'A', b'Abandoned'), (b'O', b'Ongoing'), (b'D', b'Deleted')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(default=b'O', max_length=1, choices=[(b'C', b'Completed'), (b'A', b'Abandoned'), (b'O', b'Ongoing'), (b'D', b'Deleted')]),
        ),
        migrations.AlterField(
            model_name='task',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default=b'O', max_length=1, choices=[(b'C', b'Completed'), (b'A', b'Abandoned'), (b'O', b'Ongoing'), (b'D', b'Deleted')]),
        ),
    ]
