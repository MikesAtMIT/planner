from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^calendar/$', views.calendar),
    url(r'^calendar/(?P<project>.+)/(?P<d1>[0-9]{8})-(?P<d2>[0-9]{8})/$', views.calendar),
    url(r'^calendar/(?P<d1>[0-9]{8})-(?P<d2>[0-9]{8})/$', views.calendar),
    url(r'^calendar/(?P<project>.+)/$', views.calendar),

    # ajax endpoints
    url(r'^toggle-task/$', views.toggle_task),
    url(r'^delete-task/$', views.delete_task),
    url(r'^save-new-task/$', views.save_new_task),
    url(r'^update-task/$', views.update_task),
]
