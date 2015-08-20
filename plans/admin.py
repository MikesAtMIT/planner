from django.contrib import admin
from .models import Project, Experiment, Task


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
admin.site.register(Project, ProjectAdmin)


class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'project', 'order')
admin.site.register(Experiment, ExperimentAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'experiment', 'date')
admin.site.register(Task, TaskAdmin)
