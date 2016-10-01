from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /HorizonQuiz/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.get_answer, name='results')
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.get_answer, name='results')
]
