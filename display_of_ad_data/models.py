from django.db import models
from portal.local_settings import ad_user, ad_pwd, ad_server

# Create your models here.

from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import getpass, datetime


def search_ad_data(inputSearch, typeSearch):
    #server = Server('corp.willesden.by', get_info=ALL)
    server = Server(ad_server, get_info=ALL)
    # user=input("Enter login: ")
    # pwd=getpass.getpass("Enter pasword: ")
    user = ad_user
    pwd = ad_pwd
    user = 'CORP\\' + user

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
    #(&(givenName=A*)(sn=Smith))
    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)
    entry_list = c.extend.standard.paged_search(search_base='DC=corp,DC=willesden,DC=by',
                                                search_filter='(&(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=willesden,DC=by)'+ad_filter+')',
                                                #search_filter = ad_filter,
                                                search_scope=SUBTREE,
                                                attributes=['cn', 'objectCategory', 'mail', 'sAMAccountName',
                                                            'lastLogon'],
                                                paged_size=5,
                                                generator=False)

    for i in range(3):
        del entry_list[0]

    for entry in entry_list:
        entry['dn'] = entry['dn'].split(',')[0][3:]

    #print('Total entries retrieved:', len(entry_list))
    ad_data=[]

    for entry in entry_list:
        #print(entry)
        temp = []
        if not entry['attributes']['lastLogon']:
            entry['attributes']['lastLogon'] = datetime.datetime(1601, 1, 1, tzinfo=None)
        t = entry['attributes']['lastLogon']

        if typeSearch == 'last_logon' and (
                        datetime.datetime.now().replace(tzinfo=None) - t.replace(tzinfo=None) < datetime.timedelta(days=int(inputSearch))):
            continue
        temp.append(entry['dn'])
        temp.append(t.strftime('%m/%d/%Y'))
        temp.append(entry['attributes']['sAMAccountName'])
        temp.append(entry['attributes']['mail'])
        ad_data.append(temp)

    return ad_data
