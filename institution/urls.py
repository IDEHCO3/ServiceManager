from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', None),
    url(r'^(?P<institution_id>\d+)/services/', None),
    url(r'^(?P<institution_id>\d+)/container/', None),
)
