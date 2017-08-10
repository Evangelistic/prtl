from django.conf.urls import url
from send_email import views


urlpatterns = [
    url(r'^send-email', views.send, name='Send email'),
]