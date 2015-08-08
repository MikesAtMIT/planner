# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('objective', models.TextField()),
                ('notes', models.TextField()),
                ('status', models.CharField(default=b'O', max_length=1, choices=[(b'C', b'Completed'), (b'A', b'Abandoned'), (b'O', b'Ongoing')])),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('objective', models.TextField()),
                ('notes', models.TextField()),
                ('status', models.CharField(default=b'O', max_length=1, choices=[(b'C', b'Completed'), (b'A', b'Abandoned'), (b'O', b'Ongoing')])),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('objective', models.TextField()),
                ('notes', models.TextField()),
                ('status', models.CharField(default=b'O', max_length=1, choices=[(b'C', b'Completed'), (b'A', b'Abandoned'), (b'O', b'Ongoing')])),
                ('date', models.DateField()),
                ('experiment', models.ForeignKey(to='plans.Experiment')),
            ],
        ),
        migrations.AddField(
            model_name='experiment',
            name='project',
            field=models.ForeignKey(to='plans.Project'),
        ),
    ]
