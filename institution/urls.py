from django.conf.urls import patterns, url
from institution import views

urlpatterns = patterns('',
    url(r'^(?P<initials>.+)/$', views.InstitutionDetail.as_view(), name='institution_detail'),
    url(r'^(?P<institution_initials>.+)/services/', views.ServiceListByInstitution.as_view(), name='service_list'),
    url(r'^(?P<institution_initials>.+)/services/(?P<pk>\d+)/', views.ServiceDeleteByInstitution.as_view(), name='service_delete'),
    url(r'^(?P<institution_initials>.+)/container/', views.ContainerCreate.as_view(), name='container_create'),
    url(r'^(?P<institution_initials>.+)/container/(?P<pk>\d+)/', views.ContainerDetail.as_view(), name='container_detail')
)
