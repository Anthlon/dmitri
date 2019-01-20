from django.conf.urls import url
from .views import AboutUsView, AboutEdit
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', AboutUsView.as_view(), name='about_us'),
    url(r'^edit/$', login_required(AboutEdit.as_view()), name='about_edit')
]

