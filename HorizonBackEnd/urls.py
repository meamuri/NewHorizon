from django.conf.urls import include, url
from django.contrib import admin
from HorizonQuiz import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nonAutoQuiz/', include('HorizonQuiz.urls')),

    url(r'^(?P<width>[0-9]+)/(?P<height>[0-9]+)/(?P<map_id>[0-9]+)/$', views.player_start_game),
    url(r'^(?P<width>[0-9]+)/(?P<height>[0-9]+)/$', views.player_start_game),
    url(r'^$', views.player_start_game),
    url(r'^quiz/$', views.game_center),
    url(r'^quiz/(?P<num>[0-9]+)/$', views.game_center),
    url(r'^map/$', views.get_curr_map),
]
