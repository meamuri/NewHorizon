from django.conf.urls import include, url
from django.contrib import admin
from HorizonQuiz import views, tmp_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nonAutoQuiz/', include('HorizonQuiz.urls')),
    url(r'^(?P<width>[0-9]+)/(?P<height>[0-9]+)/(?P<map_id>[0-9]+)/$', views.player_start_game),
    url(r'^(?P<width>[0-9]+)/(?P<height>[0-9]+)/$', views.player_start_game),
    url(r'^getMap/$', views.get_exist_map),

    url(r'^$', tmp_view.player_start_game),
    url(r'^quiz/$', tmp_view.game_center),
    url(r'^quiz/(?P<num>[0-9]+)/$', tmp_view.game_center),
]
