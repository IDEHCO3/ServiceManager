from django.conf.urls import url
from institution import views

urlpatterns = [
    url(r'^$', views.InstitutionList.as_view(), name='profile_list'),
    url(r'^profile/$', views.ProfileDetail.as_view(), name='profile_detail'),
    url(r'^(?P<initials>\w+)/$', views.InstitutionDetail.as_view(), name='institution_detail'),
    url(r'^(?P<institution_initials>\w+)/links/$', views.LinkListByInstitution.as_view(), name='link_list'),
    url(r'^(?P<institution_initials>\w+)/links/(?P<pk>\d+)/$', views.LinkDeleteByInstitution.as_view(), name='link_delete'),
    url(r'^(?P<institution_initials>\w+)/container/$', views.ContainerCreate.as_view(), name='container_create'),
    url(r'^(?P<institution_initials>\w+)/container/(?P<pk>\d+)/$', views.ContainerDetail.as_view(), name='container_detail')
]
