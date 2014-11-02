from django.conf.urls import patterns, url

from recom import views

urlpatterns = patterns('',
	# ex: /recom/
	url(r'^$', views.recompage, name = 'recompage'),
    url(r'^submit', views.submit, name = 'submit'),
    url(r'^result', views.result, name = 'result'),
)