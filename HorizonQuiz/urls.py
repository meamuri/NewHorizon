from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.get_question, name='index'),
    url(r'^(?P<user_answer>[1-4])/$', views.get_answer, name='results'),
    url(r'^accuracyQuestion/$', views.get_accuracy_question, name='results'),
    url(r'^accuracyQuestion/(?P<digit_of_answer>[0-9]+)/$', views.get_accuracy_answer, name='results')
]
