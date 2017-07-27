from django.shortcuts import render
from .models import search_ad_data, search_ad_data_group
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

# Create your views here.


#@login_required
@require_GET
def ad_search(request):
    try:
        inputSearch = request.GET['inputSearch']
        typeSearch=request.GET['typeSearch']
    except:
        inputSearch = ''
        typeSearch='login'
    if inputSearch == '':
        return render(request, 'portal/ad-search.html', {
            'title': 'AD Search', })
    else:
        if typeSearch == 'group':
            #categorySearch = r'Group'
            data = search_ad_data_group(inputSearch, typeSearch)
            content = {'title': 'AD Search',
                       'rowName': 'Group credentials',
                       'colName': ['Group name', 'Description', 'Member'],
                       'data': data,
                       'len': len(data)}
        else:
            #categorySearch = r'Person'
            data = search_ad_data(inputSearch, typeSearch)

            content = {'title': 'AD Search',
                       'rowName': 'User credentials',
                       'colName': ['Full name', 'Last logon', 'Login', 'Email'],
                       'data': data,
                       'len': len(data)}

        return render(request, 'portal/ad-search.html', content)


