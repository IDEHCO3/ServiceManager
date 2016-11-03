from django.conf.urls import url
from institution import views

urlpatterns = [
    url(r'^$', views.InstitutionList.as_view(), name='profile_list'),
    url(r'^profile/$', views.ProfileDetail.as_view() ,name='profile_detail'),
    url(r'^(?P<initials>\w+)/$', views.InstitutionDetail.as_view(), name='institution_detail'),
    url(r'^(?P<institution_initials>\w+)/services/$', views.ServiceListByInstitution.as_view(), name='service_list'),
    url(r'^(?P<institution_initials>\w+)/services/(?P<pk>\d+)/$', views.ServiceDeleteByInstitution.as_view(), name='service_delete'),
    url(r'^(?P<institution_initials>\w+)/container/$', views.ContainerCreate.as_view(), name='container_create'),
    url(r'^(?P<institution_initials>\w+)/container/(?P<pk>\d+)/$', views.ContainerDetail.as_view(), name='container_detail')
]
