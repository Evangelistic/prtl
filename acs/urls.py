from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^acs', views.acs, name='acs'),
]