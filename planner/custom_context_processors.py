from plans.models import Project
from django.contrib.auth.models import User


def navbar_data(request):
  projects = Project.objects.all()
  users = User.objects.all()
  context = {
    'all_projects': projects,
    'all_users': users,
  }
  return context
