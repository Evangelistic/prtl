from django.shortcuts import render
from display_ad_data.models import search_ad_data       #temparary
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

# Create your views here.


#@login_required
@require_GET
def ad_modify(request):
    try:
        inputSearch = request.GET['inputSearch']
        typeSearch=request.GET['typeSearch']
    except:
        inputSearch = ''
        typeSearch='login'
    if inputSearch == '':
        return render(request, 'portal/ad-modify.html', {
            'title': 'AD Search', })
    else:
        data = search_ad_data(inputSearch, typeSearch)
        content = {'title': 'AD Search',
                   'data': data,
                   'len': len(data)}

        return render(request, 'portal/ad-modify.html', content)


