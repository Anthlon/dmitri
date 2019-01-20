from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import WorkDoneListView, WorkDoneDetailView, WorkDoneCreate, WorkDoneUpdate, WorkDoneDelete


urlpatterns = [
    url(r'^$', WorkDoneListView.as_view(), name='work_done_list'),
    url(r'^(?P<pk>\d+)/detail/$', WorkDoneDetailView.as_view(), name='work_done_detail'),
    url(r'^add/$', login_required(WorkDoneCreate.as_view()), name='work_done_add'),
    url(r'^(?P<pk>\d+)/edit/$', login_required(WorkDoneUpdate.as_view()), name='work_done_edit'),
    url(r'^(?P<pk>\d+)/delete/$', login_required(WorkDoneDelete.as_view()), name='work_done_delete'),
]


