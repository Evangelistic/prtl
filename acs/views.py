from django.shortcuts import render_to_response
from django.conf import settings
# Create your views here.


def acs(request):
    content = {'url': settings.ACS_URL}
    return render_to_response('portal/acs.html', content)
