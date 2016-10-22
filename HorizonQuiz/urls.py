from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^enumQuest/$', views.get_enum_question, name='index'),
    url(r'^enumQuest/(?P<user_answer>[1-4])/$', views.get_enum_answer, name='results'),
    url(r'^accuracyQuest/$', views.get_accuracy_question, name='results'),
    url(r'^accuracyQuest/(?P<digit_of_answer>[0-9]+)/$', views.get_accuracy_answer, name='results')
]
