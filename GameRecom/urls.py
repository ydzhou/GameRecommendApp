from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GameRecom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^recom/', include('recom.urls', namespace='recom')),
    url(r'^admin/', include(admin.site.urls)),
    
)
