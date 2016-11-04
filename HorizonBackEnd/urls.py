from django.conf.urls import url
from django.contrib import admin
from HorizonQuiz import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^quiz/', include('HorizonQuiz.urls')),
    url(r'^quiz/', views.game_center),
]
