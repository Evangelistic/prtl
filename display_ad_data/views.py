from django.shortcuts import render
from .models import search_ad_data, search_ad_data_group, compare_user_group
from django.views.decorators.http import require_GET

# from django.contrib.auth.decorators import login_required
# Create your views here.


# @login_required
@require_GET
def ad_search(request):
    try:
        input_search = request.GET['input_search']
        type_search = request.GET['type_search']
    except:
        input_search = ''
        type_search = 'login'
    if input_search == '':
        return render(request, 'portal/ad-search.html', {
            'title': 'AD Search', })
    else:
        if type_search == 'compare':
            input_search = input_search.split()
            data = compare_user_group(input_search)
            magic_set = set([])
            for i in data:
                magic_set.update(data[i])
            magic_list = []
            for i in magic_set:
                temp = [[i]]
                for j in data:
                    if i in data[j]:
                        temp.append(['+'])
                    else:
                        temp.append(['-'])
                magic_list.append(temp)
            content = {'title': 'Compare AD User',
                       'rowName': 'Compare User Group',
                       'colName': ['Group name'] + input_search,
                       'data': magic_list,
                       'len': len(data)}
            render(request, 'portal/ad-search.html', content)
        elif type_search == 'group':
            data = search_ad_data_group(input_search, type_search)
            content = {'title': 'AD Search',
                       'rowName': 'Group credentials',
                       'colName': ['Group name', 'Description', 'Member'],
                       'data': data,
                       'len': len(data)}
        else:
            data = search_ad_data(input_search, type_search)
            '''delete  dn user attribute  in output'''
            data = [data[i][1:] for i in range(len(data))]
            content = {'title': 'AD Search',
                       'rowName': 'User credentials',
                       'colName': ['Full name', 'Last logon', 'Login', 'Email'],
                       'data': data,
                       'len': len(data)}

        return render(request, 'portal/ad-search.html', content)
