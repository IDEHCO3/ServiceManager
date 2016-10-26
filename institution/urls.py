from django.conf.urls import patterns, url
from institution import views

urlpatterns = patterns('',
    url(r'^(?P<initials>\w+)/$', views.InstitutionDetail.as_view(), name='institution_detail'),
    url(r'^(?P<institution_initials>\w+)/services/$', views.ServiceListByInstitution.as_view(), name='service_list'),
    url(r'^(?P<institution_initials>\w+)/services/(?P<pk>\d+)/$', views.ServiceDeleteByInstitution.as_view(), name='service_delete'),
    url(r'^(?P<institution_initials>\w+)/container/$', views.ContainerCreate.as_view(), name='container_create'),
    url(r'^(?P<institution_initials>\w+)/container/(?P<pk>\d+)/$', views.ContainerDetail.as_view(), name='container_detail')
)
