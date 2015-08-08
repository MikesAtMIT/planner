from django.contrib import admin
from .models import Project, Experiment, Task

admin.site.register(Project)
admin.site.register(Experiment)
admin.site.register(Task)
