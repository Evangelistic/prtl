from django.conf.urls import url, include
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
]