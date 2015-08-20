# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copy_experiment_primary_keys_to_order(apps, schema_editor):
    Experiment = apps.get_model('plans', 'Experiment')
    for experiment in Experiment.objects.all():
        experiment.order = experiment.pk
        experiment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_experiment_order'),
    ]

    operations = [
        migrations.RunPython(copy_experiment_primary_keys_to_order)
    ]
