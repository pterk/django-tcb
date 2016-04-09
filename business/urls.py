from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.entry,
        name='business-entry'
    ),
    url(
        regex=r'^overview/$',
        view=views.overview,
        name='business-overview',
    ),
]
