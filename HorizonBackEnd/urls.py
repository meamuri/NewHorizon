from django.conf.urls import include, url
from django.contrib import admin
from HorizonQuiz import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^getMap/$', views.get_play_map),
    url(r'^getMap/(?P<width>[0-9]+)/(?P<height>[0-9]+)/$', views.get_play_map),
    url(r'^quiz/', include('HorizonQuiz.urls')),
    url(r'^startGame/$', views.init_game)
]
