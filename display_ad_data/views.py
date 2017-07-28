from django.shortcuts import render
from .models import search_ad_data, search_ad_data_group, compare_user_group
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
        if typeSearch == 'compare':
            inputSearch = inputSearch.split()
            print(inputSearch)
            data = compare_user_group(inputSearch)
            print(len(data['vlva']))
            print(len(data['das']))
            magicset = set([])
            for i in data:
                print(data[i][0])
                magicset.update(data[i])
            magiclist = []
            for i in magicset:
                temp = [[i]]
                for j in data:
                    if i in data[j]:
                        temp.append('+')
                    else:
                        temp.append('-')
                magiclist.append(temp)
            content = {'title': 'Compare AD User',
                       'rowName': 'Compare User Group',
                       'colName': ['Group name'] + inputSearch,
                       'data': magiclist,
                       'len': len(data)}
            render(request, 'portal/ad-search.html', content)
        elif typeSearch == 'group':
            data = search_ad_data_group(inputSearch, typeSearch)
            content = {'title': 'AD Search',
                       'rowName': 'Group credentials',
                       'colName': ['Group name', 'Description', 'Member'],
                       'data': data,
                       'len': len(data)}
        else:
            data = search_ad_data(inputSearch, typeSearch)
            '''delete  dn user attribute  in output'''
            data = [data[i][1:] for i in range(len(data))]
            content = {'title': 'AD Search',
                       'rowName': 'User credentials',
                       'colName': ['Full name', 'Last logon', 'Login', 'Email'],
                       'data': data,
                       'len': len(data)}

        return render(request, 'portal/ad-search.html', content)


