from django.conf.urls import url
from acs_logs import views

urlpatterns = [
    url(r'^acs-search', views.acs_search, name='ACS Searh'),
]