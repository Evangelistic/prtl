from django.conf import settings
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import datetime

# from django.db import models
# import getpass
# Create your models here.

AD_ATTRIBUTE = {
    'login': 'sAMAccountName',
    'full_name': 'cn',
    'last_logon': 'lastLogon',
    'email': 'mail',
    'group': 'cn',
}

temp = []


def search_ad_data(input_search, type_search):
    """
    AD_SERVER_LS: ldap server
    AD_BASE_LS: ldap server, base for search
    AD_USER_LS: ldap user for auth
    AD_PWD_LS: password for auth
    :param input_search:
    :param type_search:
    :return:
    """
    server = Server(settings.AD_SERVER_LS, get_info=ALL)
    user = settings.AD_USER_LS
    pwd = settings.AD_PWD_LS
    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)

    if type_search == 'last_logon':
        ad_filter = '('+AD_ATTRIBUTE[type_search]+'=*)'
    else:
        ad_filter = '(' + AD_ATTRIBUTE[type_search] + '=' + input_search + ')'

    entry_list = c.extend.standard.paged_search(
        search_base=settings.AD_BASE_LS,
        search_filter='(&(objectCategory=CN=Person,CN=Schema,CN=Configuration,' + settings.AD_BASE_LS + ')' +
                      ad_filter + ')',
        search_scope=SUBTREE,
        attributes=['cn', 'objectCategory', 'mail', 'sAMAccountName', 'lastLogon'],
        paged_size=5,
        generator=False)

    for i in range(3):
        del entry_list[0]

    ad_data = []
    for entry in entry_list:

        if not entry['attributes']['lastLogon']:
            entry['attributes']['lastLogon'] = datetime.datetime(1601, 1, 1, tzinfo=None)
        t = entry['attributes']['lastLogon']

        if type_search == 'last_logon' and (
                        datetime.datetime.now().replace(tzinfo=None) - t.replace(tzinfo=None)
                        <
                        datetime.timedelta(days=int(input_search))
        ):
            continue
        temp.append([entry['dn']])
        entry['dn'] = entry['dn'].split(',')[0][3:]
        temp.append([entry['dn']])
        temp.append([t.strftime('%m/%d/%Y')])
        temp.append([entry['attributes']['sAMAccountName']])
        temp.append([entry['attributes']['mail']])
        ad_data.append(temp)

    return ad_data


def search_ad_data_group(input_search, type_search):
    """
    AD_SERVER_LS: ldap server
    AD_BASE_LS: ldap server, base for search
    AD_USER_LS: ldap user for auth
    AD_PWD_LS: password for auth
    :param input_search:
    :param type_search:
    :return:
    """
    server = Server(settings.AD_SERVER_LS, get_info=ALL)
    user = settings.AD_USER_LS
    pwd = settings.AD_PWD_LS

    ad_filter = '(' + AD_ATTRIBUTE[type_search] + '=' + input_search + ')'

    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)
    entry_list = c.extend.standard.paged_search(
        search_base=settings.AD_BASE_LS,
        search_filter='(&(objectCategory=CN=Group,CN=Schema,CN=Configuration,' + settings.AD_BASE_LS + ')' +
                      ad_filter + ')',
        search_scope=SUBTREE,
        attributes=['cn', 'description', 'member', 'whenChanged', 'whenCreated'],
        paged_size=5,
        generator=False)

    for i in range(3):
        del entry_list[0]

    for entry in entry_list:
        entry['dn'] = entry['dn'].split(',')[0][3:]

    ad_data = []

    for entry in entry_list:

        temp.append([entry['attributes']['cn']])
        temp.append(entry['attributes']['description'])
        """change member view"""
        list_members = []
        for member in entry['attributes']['member']:
            list_members.append(member[3:].split(sep=',')[0])
        temp.append(list_members)
        ad_data.append(temp)

    return ad_data


def compare_user_group(input_search):
    """
    AD_SERVER_LS: ldap server
    AD_BASE_LS: ldap server, base for search
    AD_USER_LS: ldap user for auth
    AD_PWD_LS: password for auth
    :param input_search:
    :return:
    """
    server = Server(settings.AD_SERVER_LS, get_info=ALL)
    user = settings.AD_USER_LS
    pwd = settings.AD_PWD_LS
    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)
    ad_data = {}
    for ad_login in input_search:
        cn = search_ad_data(ad_login, 'login')[0][0][0]
        print(cn)
        ad_filter = '(member=' + cn + ')'

        entry_list = c.extend.standard.paged_search(
            search_base=settings.AD_BASE_LS,
            search_filter='(&(objectCategory=CN=Group,CN=Schema,CN=Configuration,' + settings.AD_BASE_LS + ')' +
                          ad_filter + ')',
            search_scope=SUBTREE,
            attributes=['cn', 'description', 'member', 'whenChanged', 'whenCreated'],
            paged_size=5,
            generator=False)

        for i in range(3):
            del entry_list[0]

        for entry in entry_list:
            entry['dn'] = entry['dn'].split(',')[0][3:]
        for entry in entry_list:
            temp.append(entry['attributes']['cn'])
        ad_data[ad_login] = temp

    return ad_data
