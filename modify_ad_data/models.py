from django.conf import settings
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE, MODIFY_REPLACE, MODIFY_ADD

# from django.db import models
# Create your models here.


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

    server = Server(settings.AD_SERVER_LS, get_info=ALL)
    user = settings.AD_USER_LS
    pwd = settings.AD_PWD_LS
    attr = settings.AD_ATTR_LS
    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)
    entry_list = c.extend.standard.paged_search(
        search_base=settings.AD_BASE_LS,
        search_filter='(&(objectCategory=CN=' +
                      type_object +
                      ',CN=Schema,CN=Configuration,' + settings.AD_BASE_LS + ')(' +
                      type_search + '=' + who_is + '))',
        search_scope=SUBTREE,
        attributes=attr[type_object],
        paged_size=5,
        generator=False)

    c.unbind()

    for i in range(3):
        del entry_list[0]

    if len(entry_list) > 1:
        return ''
    else:
        return entry_list


def modify_in_ad(data_dn, type_attribute, new_value_attr):
    """
    AD_ATTR_LS: dict for changing return object attr
    AD_SERVER_LS: ldap server
    AD_BASE_LS: ldap server, base for search
    AD_USER_LS: ldap user for auth
    AD_PWD_LS: password for auth
    :param data_dn: this dict contains ad user data who we want changing
    :param type_attribute: type of attribute
    :param new_value_attr: new value ad attribute who we want to change
    :return:
    """

    server = Server(settings.AD_SERVER_LS, get_info=ALL)
    user = settings.AD_USER_LS
    pwd = settings.AD_PWD_LS
    c = Connection(server, user=user, password=pwd, authentication=NTLM, auto_bind=True)

    try:
        if type_attribute == 'cn':
            new_value_attr = 'CN=' + new_value_attr

            c.modify_dn(
                data_dn['distinguishedName'],
                new_value_attr,
            )
        elif data_dn[type_attribute]:
            c.modify(
                data_dn['distinguishedName'], {
                    type_attribute: [(MODIFY_REPLACE, [new_value_attr])]
                }
            )
        else:
            c.modify(
                data_dn['distinguishedName'], {
                    type_attribute: [(MODIFY_ADD, [new_value_attr])]
                }
            )
    except Warning:
        print('function modify_in_ad failed')

    c.unbind()
