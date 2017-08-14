from django.shortcuts import render
from django.views.decorators.http import require_GET
import csv
from portal.settings import AD_USER_LS, AD_PWD_LS, AD_SERVER_LS, AD_BASE_LS, AD_ATTR_LS
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
# Create your views here.

@require_GET
def logons(request):
    try:
        input_search = request.GET['input_search']
        type_search = request.GET['type_search']
    except:
        input_search = ''
        type_search = 'full_name'
    out = []
    if type_search == 'login':
        try:
            user = search_in_ad('Person', 'sAMAccountName', input_search)
            full_name = user[0]['attributes']['cn']
        except:
            full_name = ''
        if full_name != '':
            with open('//mo02vdc01/compusers$/NameUserComp.txt',"r", newline="") as file:
                logons = csv.reader((x.replace('\0', '') for x in file),delimiter=';')
                for logon in logons:
                    if len(logon) > 2 and logon[0][5:].strip() == input_search.strip():
                        out.append([logon[0][5:], logon[1][15:], logon[2][13:]])
            content = {
                'name' : full_name,
                'data' : list(reversed(out)),
            }
        else:
            out.append(['No data','No data'])
            content = {
                'name': full_name,
                'data': list(reversed(out)),
            }
        return render(request, 'portal/logons.html', content)
    elif type_search == 'full_name':
        try:
            user = search_in_ad('Person', 'cn', input_search)
        except:
            out.append(['Error', 'Error'])
            content = {
                'name': '',
                'data': list(reversed(out)),
            }
            return render(request, 'portal/logons.html', content)
        if len(user) > 1:
            for u in user:
                out.append(u['attributes']['cn'])
            for user in out:
                print(user)
            content = {
                'name': 'Найдено несколько пользователей',
                'data': out,
                'users' : 'True',
            }
            return render(request, 'portal/logons.html', content)
        if user != []:
            user_login = user[0]['attributes']['sAMAccountName']
            full_name = user[0]['attributes']['cn']
            if user_login != '':
                with open('//mo02vdc01/compusers$/NameUserComp.txt', "r", newline="") as file:
                    logons = csv.reader((x.replace('\0', '') for x in file), delimiter=';')
                    for logon in logons:
                        if len(logon) > 2 and logon[0][5:].strip() == user_login.strip():
                            out.append([logon[0][5:],logon[1][15:], logon[2][13:]])
                content = {
                    'name': full_name,
                    'data': list(reversed(out)),
                }
        else:
            out.append(['No data', 'No data'])
            content = {
                'name': '',
                'data': list(reversed(out)),
            }
        return render(request, 'portal/logons.html', content)
    elif type_search == 'pc':
        with open('//mo02vdc01/compusers$/NameUserComp.txt', "r", newline="") as file:
            logons = csv.reader((x.replace('\0', '') for x in file), delimiter=';')
            for logon in logons:
                if len(logon) > 2 and logon[1][15:].strip() == input_search.strip().upper():
                    out.append([logon[0][5:], logon[1][15:], logon[2][13:]])
                    content = {
                        'name': input_search,
                        'data': list(reversed(out)),
                    }
            if out == []:
                out.append(['No data', 'No data'])
                content = {
                    'name': '',
                    'data': list(reversed(out)),
                }
            return render(request,'portal/logons.html',content)


def search_in_ad(type_object, type_search, who_is):
    """
    AD_ATTR_LS: dict for changing return object attr
    AD_SERVER_LS: ldap server
    AD_BASE_LS: ldap server, base for search
    AD_USER_LS: ldap user for auth
    AD_PWD_LS: password for auth
    :param type_object: Person, Group
    :param type_search: sAMAccountName, lastLogon, cn, dn
    :param who_is: value of type_search
    :return: dn value, this function return only one user data
    """
    server = Server(AD_SERVER_LS, get_info=ALL)
    user = AD_USER_LS
    pwd = AD_PWD_LS
    attr = AD_ATTR_LS
    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)
    entry_list = c.extend.standard.paged_search(
        search_base=AD_BASE_LS,
        search_filter='(&(objectCategory=CN=' +
                      type_object +
                      ',CN=Schema,CN=Configuration,' + AD_BASE_LS + ')(' +
                      type_search + '=' + who_is + '))',
        search_scope=SUBTREE,
        attributes=attr[type_object],
        paged_size=5,
        generator=False)

    c.unbind()

    for i in range(3):
        del entry_list[0]
    return entry_list
