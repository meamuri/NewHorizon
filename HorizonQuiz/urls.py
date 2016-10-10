from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_answer>[0-9]+)/$', views.get_answer, name='results')
]
