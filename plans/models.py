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
    order = models.PositiveIntegerField(unique=True)

    objects = ExperimentManager()

    def update_order(self, new_order):
        old_order = self.order
        self.order = 0
        self.save()     # to preserve uniqueness of order field

        up = new_order > old_order      # whether you're going up or down in order
        next_order = old_order
        list_of_updated_experiments = []

        while next_order != new_order:
            next_order = next_order + 1 if up else next_order - 1
            next_experiment = type(self).objects.get(order=next_order)
            next_experiment.order = next_order - 1 if up else next_order + 1
            next_experiment.save()
            list_of_updated_experiments.append(next_experiment)
        self.order = new_order
        self.save()
        list_of_updated_experiments.append(self)
        return list_of_updated_experiments
    
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
