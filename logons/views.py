from django.shortcuts import render
from django.views.decorators.http import require_GET
from portal.settings import LOGONS_LOCAL_LOG_DIR, LOGONS_FILE_NAME
import csv
from logons.models import search_in_ad, sync_file_logs

# Create your views here.


@require_GET
def logons(request):
    content = {'table_flag': True}
    try:
        input_search = request.GET['input_search']
        type_search = request.GET['type_search']
    except NameError:
        content = {'name': '', 'table_flag': True}
        return render(request, 'portal/logons.html', content)
    sync = sync_file_logs()
    if sync:
        log_file = LOGONS_LOCAL_LOG_DIR + '\\' + LOGONS_FILE_NAME
        out = []
        if type_search == 'login':
            try:
                user = search_in_ad('Person', 'sAMAccountName', input_search)
                full_name = user[0]['attributes']['cn']
            except NameError:
                full_name = ''
            if full_name != '':
                with open(log_file, "r", newline="") as file:
                    user_logons = csv.reader((x.replace('\0', '') for x in file), delimiter=';')
                    for logon in user_logons:
                        if len(logon) > 2 and logon[0][5:].strip() == input_search.strip():
                            out.append([logon[0][5:], logon[1][15:], logon[2][13:]])
                content = {
                    'name': full_name,
                    'data': list(reversed(out)),
                }
            else:
                content = {
                    'name': 'Пользователь с таким логином не найден',
                    'table_flag': True
                }
            return render(request, 'portal/logons.html', content)
        elif type_search == 'full_name':
            try:
                user = search_in_ad('Person', 'cn', input_search)
            except NameError:
                out.append(['Error', 'Error', 'Error'])
                content = {
                    'name': '',
                    'data': list(reversed(out)),
                }
                return render(request, 'portal/logons.html', content)
            if len(user) > 1:
                for u in user:
                    out.append(u['attributes']['cn'])
                content = {
                    'name': 'Найдено несколько пользователей',
                    'data': out,
                    'table_flag': True,
                }
                return render(request, 'portal/logons.html', content)
            if user:
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
                    'name': 'Пользователь с таким именем не найден',
                    'table_flag': True,
                }
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
                        'name': 'ПК с такими именем не найден',
                        'table_flag': True,
                    }
                return render(request, 'portal/logons.html', content)
    else:
        content = {
            'name': 'Не удалось получить информацию',
            'table_flag': True,
        }
        return render(request, 'portal/logons.html', content)
