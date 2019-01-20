from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import PersonalArea, UserListView, UserDetailView

urlpatterns = [
    url(r'^$', login_required(PersonalArea.as_view()), name='personal_area'),
    url(r'^user_list/$', login_required(UserListView.as_view()), name='user_list'),
    url(r'^user_list/(?P<pk>\d+)$', login_required(UserDetailView.as_view()), name='user_detail_view'),
]


