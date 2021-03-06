# coding=utf-8
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.conf import settings
import csv
from logons.models import search_in_ad, sync_file_logs

# Create your views here.


@require_GET
def logons(request):
    content = {'table_flag': True}
    input_search = request.GET.get('input_search', False)
    type_search = request.GET.get('type_search', False)
    sync = sync_file_logs()
    if sync:
        log_file = settings.LOGONS_LOCAL_LOG_DIR + '\\' + settings.LOGONS_FILE_NAME
        out = []
        if type_search == 'login':
            user = search_in_ad('Person', 'sAMAccountName', input_search)
            if len(user) == 1:
                full_name = user[0]['attributes']['cn']
                with open(log_file, "r", newline="") as file:
                    user_logons = csv.reader((x.replace('\0', '') for x in file), delimiter=';')
                    for logon in user_logons:
                        if len(logon) > 2 and logon[0][5:].strip() == input_search.strip():
                            out.append([logon[0][5:], logon[1][15:], logon[2][13:]])
                content = {
                    'name': full_name,
                    'data': list(reversed(out)),
                }
            elif len(user) > 1:
                content = {
                    'name': 'Найдено больше одного пользователя. Уточните запрос.',
                    'table_flag': True
                }
            else:
                content = {
                    'name': 'Пользователь с таким логином не найден.',
                    'table_flag': True
                }
            content.update({'type_search': type_search})
            content.update({'text': input_search})
            content.update({'search': '<span class="fa fa-user">Search By Login</span>'})
            return render(request, 'portal/logons.html', content)
        elif type_search == 'full_name':
            try:
                user = search_in_ad('Person', 'cn', input_search)
            except NameError:
                content = {
                    'name': 'Error',
                    'table_flag': True
                }
                content.update({'type_search': type_search})
                content.update({'text': input_search})
                content.update({'search': '<span class="fa fa-address-card">Search By Full name</span>'})
                return render(request, 'portal/logons.html', content)
            if len(user) > 1:
                for u in user:
                    out.append(u['attributes']['cn'])
                content = {
                    'name': 'Найдено несколько пользователей.',
                    'data': out,
                    'table_flag': True,
                }
                content.update({'type_search': type_search})
                content.update({'text': input_search})
                content.update({'search': '<span class="fa fa-address-card">Search By Full name</span>'})
                return render(request, 'portal/logons.html', content)
            if len(user) == 1:
                user_login = user[0]['attributes']['sAMAccountName']
                full_name = user[0]['attributes']['cn']
                if user_login != '':
                    with open(log_file, "r", newline="") as file:
                        user_logons = csv.reader((x.replace('\0', '') for x in file), delimiter=';')
                        for logon in user_logons:
                            if len(logon) > 2 and logon[0][5:].strip() == user_login.strip():
                                out.append([logon[0][5:], logon[1][15:], logon[2][13:]])
                    content = {
                        'name': full_name,
                        'data': list(reversed(out)),
                    }
            else:
                content = {
                    'name': 'Пользователь с таким именем не найден.',
                    'table_flag': True,
                }
            content.update({'type_search': type_search})
            content.update({'text': input_search})
            content.update({'search': '<span class="fa fa-address-card">Search By Full name</span>'})
            return render(request, 'portal/logons.html', content)
        elif type_search == 'pc':
            with open(log_file, "r", newline="") as file:
                user_logons = csv.reader((x.replace('\0', '') for x in file), delimiter=';')
                for logon in user_logons:
                    if len(logon) > 2 and logon[1][15:].strip() == input_search.strip().upper():
                        out.append([logon[0][5:], logon[1][15:], logon[2][13:]])
                        content = {
                            'name': input_search,
                            'data': list(reversed(out)),
                        }
                if not out:
                    content = {
                        'name': 'ПК с такими именем не найден.',
                        'table_flag': True,
                    }
                content.update({'type_search': type_search})
                content.update({'text': input_search})
                content.update({'search': '<span class="fa fa-desktop">Search By PC</span>'})
                return render(request, 'portal/logons.html', content)
        else:
            content = {'name': '',
                       'table_flag': True,
                       'type_search': 'full_name',
                       'search': '<span class="fa fa-address-card">Search By Full name</span>',
                       'text': ''
                       }
            return render(request, 'portal/logons.html', content)
    else:
        content = {
            'name': 'Не удалось получить информацию.',
            'table_flag': True,
        }
        return render(request, 'portal/logons.html', content)
