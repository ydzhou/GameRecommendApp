from django.conf.urls import patterns, url

from GameRecomForSteam import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        )
