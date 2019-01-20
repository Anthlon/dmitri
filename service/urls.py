from django.conf.urls import url
from .views import ServiceTypeEdit, ServiceMainView, ServiceTypeView, ServiceTypeSingleEdit, ServiceAdd, ServiceView, \
    ServiceEdit, ServiceDelete


urlpatterns = [
    url(r'^$', ServiceMainView.as_view(), name='service_main'),
    url(r'^add/$', ServiceAdd.as_view(), name='service_add'),
    url(r'^(?P<pk>\d+)/detail/$', ServiceView.as_view(), name='service_detail'),
    url(r'^(?P<pk>\d+)/edit/$', ServiceEdit.as_view(), name='service_edit'),
    url(r'^(?P<pk>\d+)/delete/$', ServiceDelete.as_view(), name='service_delete'),
    url(r'^(?P<pk>\d+)/type/$', ServiceTypeView.as_view(), name='service_type'),
    url(r'^(?P<pk>\d+)/type_single_edit/$', ServiceTypeSingleEdit.as_view(), name='service_type_single_edit'),
    url(r'^type_edit/$', ServiceTypeEdit.as_view(), name='service_type_edit'),
]

