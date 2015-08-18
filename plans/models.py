from django.db import models


COMPLETED = 'C'
ABANDONED = 'A'
ONGOING = 'O'
DELETED = 'D'
STATUS_CHOICES = (
    (COMPLETED, 'Completed'),
    (ABANDONED, 'Abandoned'),
    (ONGOING, 'Ongoing'),
    (DELETED, 'Deleted'),
    )


class Project(models.Model):
    name = models.CharField(max_length=200)
    objective = models.TextField()
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length = 1,
        choices = STATUS_CHOICES,
        default = ONGOING,
        )

    def __unicode__(self):
        return self.name


class ExperimentManager(models.Manager):
    def create_experiment(self,name,objective,notes,project_id):
        experiment = self.create(name=name, objective=objective, notes=notes, project_id=project_id)
        experiment.order = experiment.pk
        experiment.save()
        return experiment


class Experiment(models.Model):
    name = models.CharField(max_length=200)
    objective = models.TextField()
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length = 1,
        choices = STATUS_CHOICES,
        default = ONGOING,
        )
    project = models.ForeignKey(Project)
    order = models.PositiveIntegerField(default=0)

    objects = ExperimentManager()

    def __unicode__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=200)
    # objective = models.TextField()
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length = 1,
        choices = STATUS_CHOICES,
        default = ONGOING,
        )
    date = models.DateField()
    experiment = models.ForeignKey(Experiment)

    def __unicode__(self):
        return self.name
