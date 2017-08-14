"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from portal_core import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    url(r'^$', views.index, name='Index'),
    url(r'^404$', views.error404, name='404'),
    url(r'^about-us$', views.about_us, name='About us'),
    url(r'^blog$', views.blog, name='Blog'),
    url(r'^blog-item$', views.blog_item, name='Blog item'),
    url(r'^contact-us$', views.contact_us, name='Contact us'),
    url(r'^index$', views.index, name='Index'),
    url(r'^portfolio$', views.portfolio, name='Portfolio'),
    url(r'^pricing$', views.pricing, name='Pricing'),
    url(r'^services$', views.services, name='Services'),
    url(r'^shortcodes$', views.shortcodes, name='ShortCodes'),
    url(r'^logons$', views.logons, name='Logons'),
]