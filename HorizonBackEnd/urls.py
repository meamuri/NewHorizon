from django.conf.urls import include, url
from django.contrib import admin
from HorizonQuiz import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^quiz/', include('HorizonQuiz.urls')),
]
