from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='pages/index.html'), name='index'),
    url(r'^signup/$', TemplateView.as_view(template_name='pages/signup.html'), name='signup'),
    url(r'^personal/$', TemplateView.as_view(template_name='pages/personal.html'), name='personal'),
)
