from django.db import models
from portal.local_settings import ad_user, ad_pwd, ad_server

# Create your models here.
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import getpass, datetime


def search_ad_data(inputSearch, typeSearch):
    server = Server(ad_server, get_info=ALL)
    user = ad_user
    pwd = ad_pwd

    attrSearch={
        'login': 'sAMAccountName',
        'full_name': 'cn',
        'last_logon': 'lastLogon',
        'email': 'mail',
                }

    if typeSearch == 'last_logon':
        ad_filter = '('+attrSearch[typeSearch]+'=*)'
    else:
        ad_filter = '(' + attrSearch[typeSearch] + '=' + inputSearch + ')'

    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)
    entry_list = c.extend.standard.paged_search(search_base='DC=corp,DC=willesden,DC=by',
                                                search_filter='(&(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=willesden,DC=by)'+ad_filter+')',
                                                search_scope=SUBTREE,
                                                attributes=['cn', 'objectCategory', 'mail', 'sAMAccountName',
                                                            'lastLogon'],
                                                paged_size=5,
                                                generator=False)

    for i in range(3):
        del entry_list[0]

    ad_data=[]
    for entry in entry_list:
        temp = []
        if not entry['attributes']['lastLogon']:
            entry['attributes']['lastLogon'] = datetime.datetime(1601, 1, 1, tzinfo=None)
        t = entry['attributes']['lastLogon']

        if typeSearch == 'last_logon' and (
                        datetime.datetime.now().replace(tzinfo=None) - t.replace(tzinfo=None) < datetime.timedelta(days=int(inputSearch))):
            continue
        temp.append([entry['dn']])
        entry['dn'] = entry['dn'].split(',')[0][3:]
        temp.append([entry['dn']])
        temp.append([t.strftime('%m/%d/%Y')])
        temp.append([entry['attributes']['sAMAccountName']])
        temp.append([entry['attributes']['mail']])
        ad_data.append(temp)

    return ad_data


def search_ad_data_group(inputSearch, typeSearch):
    server = Server(ad_server, get_info=ALL)
    # user=input("Enter login: ")
    # pwd=getpass.getpass("Enter pasword: ")
    user = ad_user
    pwd = ad_pwd

    attrSearch = {
        'group': 'cn',
                }
    ad_filter = '(' + attrSearch[typeSearch] + '=' + inputSearch + ')'

    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)
    entry_list = c.extend.standard.paged_search(search_base='DC=corp,DC=willesden,DC=by',
                                                search_filter='(&(objectCategory=CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=willesden,DC=by)'+ad_filter+')',
                                                search_scope=SUBTREE,
                                                attributes=['cn', 'description', 'member', 'whenChanged',
                                                            'whenCreated'],
                                                paged_size=5,
                                                generator=False)

    for i in range(3):
        del entry_list[0]

    for entry in entry_list:
        entry['dn'] = entry['dn'].split(',')[0][3:]

    ad_data = []

    for entry in entry_list:
        temp = []
        temp.append([entry['attributes']['cn']])
        temp.append(entry['attributes']['description'])
        """change member view"""
        listmembers = []
        for member in entry['attributes']['member']:
            listmembers.append(member[3:].split(sep=',')[0])
        temp.append(listmembers)
        ad_data.append(temp)

    return ad_data


def compare_user_group(inputSearch):
    server = Server(ad_server, get_info=ALL)
    user = ad_user
    pwd = ad_pwd
    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)
    ad_data = {}
    for adlogin in inputSearch:
        cn = search_ad_data(adlogin, 'login')[0][0][0]
        print(cn)
        ad_filter = '(member=' + cn + ')'

        entry_list = c.extend.standard.paged_search(search_base='DC=corp,DC=willesden,DC=by',
                                                    search_filter='(&(objectCategory=CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=willesden,DC=by)' + ad_filter + ')',
                                                    search_scope=SUBTREE,
                                                    attributes=['cn', 'description', 'member', 'whenChanged',
                                                                'whenCreated'],
                                                    paged_size=5,
                                                    generator=False)

        for i in range(3):
            del entry_list[0]

        for entry in entry_list:
            entry['dn'] = entry['dn'].split(',')[0][3:]
        temp = []
        for entry in entry_list:
            temp.append(entry['attributes']['cn'])
        ad_data[adlogin] = temp

    return ad_data
