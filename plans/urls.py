from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^calendar/$', views.calendar),
    url(r'^toggle-task/$', views.toggle_task),
    url(r'^delete-task/$', views.delete_task),
    url(r'^save-new-task/$', views.save_new_task),
    url(r'^update-task/$', views.update_task),
]
