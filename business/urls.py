from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.overview,
        name='business-overview'
    ),
    url(
        regex=r'^project/(?P<project_id>\d+)/$',
        view=views.project_overview,
        name='business-project-overview'
    ),
]
