from django.contrib import admin
from .models import Project, Experiment, Task, UserProfile


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'contributor_list')
admin.site.register(Project, ProjectAdmin)


class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'project', 'order', 'contributor_list')
admin.site.register(Experiment, ExperimentAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'experiment', 'date', 'contributor_list')
admin.site.register(Task, TaskAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
admin.site.register(UserProfile, UserProfileAdmin)
