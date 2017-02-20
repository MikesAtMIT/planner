from django.forms import ModelForm

from plans.models import Project


class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'objective',
            'notes',
        ]
