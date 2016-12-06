from django.conf.urls import url
from institution import views

urlpatterns = [
    url(r'^$', views.InstitutionList.as_view(), name='profile_list'),
    url(r'^profile/$', views.ProfileDetail.as_view(), name='profile_detail'),
    url(r'^(?P<initials>\w+)/$', views.InstitutionDetail.as_view(), name='institution_detail'),

    url(r'^(?P<institution_initials>\w+)/links/$', views.LinkListByInstitution.as_view(), name='link_list'),
    url(r'^(?P<institution_initials>\w+)/links/(?P<pk>\d+)/$', views.LinkDeleteByInstitution.as_view(), name='link_delete'),

    #url(r'^services/$', views.ServiceList.as_view()),
    #url(r'^(?P<institution_initials>\w+)/services/$', views.ServiceList.as_view()),
    #url(r'^(?P<institution_initials>\w+)/links/(?P<link_id>\d+)/services/$', views.ServiceList.as_view()),

    url(r'^(?P<institution_initials>\w+)/container/$', views.ContainerList.as_view(), name='container_create'),
    url(r'^(?P<institution_initials>\w+)/container/(?P<pk>\d+)/$', views.ContainerDetail.as_view(), name='container_detail'),

    url(r'^(?P<institution_initials>\w+)/container/controls/(?P<container>api)/$', views.ContainerControls.as_view(), name='container_control_api'),
    url(r'^(?P<institution_initials>\w+)/container/controls/(?P<container>geonode)/$', views.ContainerControls.as_view(), name='container_control_geonode'),
]
