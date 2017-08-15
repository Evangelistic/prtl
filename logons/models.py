# from django.db import models
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import socket
import os
from smb.SMBConnection import SMBConnection
import logging
from portal.settings import AD_USER_LS, AD_PWD_LS, AD_SERVER_LS, AD_BASE_LS, AD_ATTR_LS, LOGONS_LOG_DIR, \
    LOGONS_LOGON_SHARE, LOGONS_PASSWORD, LOGONS_SERVER, LOGONS_USERNAME, LOGONS_LOCAL_LOG_DIR


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


class Smb(object):
    def __init__(self, username, password, server, share, port=445):
        # split username if it contains a domain (domain\username)
        domain, username = username.split('\\') if username.count('\\') == 1 else ('', username)
        # setup data
        self.domain = str(domain)
        self.username = str(username)
        self.password = str(password)
        self.client = socket.gethostname()
        self.server = str(server)
        self.server_ip = socket.gethostbyname(server)
        self.share = str(share)
        self.port = port
        self.conn = None
        self.connected = False
        # SMB.SMBConnection logs too much
        smb_logger = logging.getLogger('SMB.SMBConnection')
        smb_logger.setLevel(logging.WARNING)

    def __str__(self):
        return dict(
            domain=self.domain,
            username=self.username,
            password=self.password,
            client=self.client,
            server=self.server,
            server_ip=self.server_ip,
            share=self.share,
            port=self.port,
            conn=self.conn,
            connected=self.connected,
        ).__str__()

    def connect(self):
        try:

            self.conn = SMBConnection(username=self.username, password=self.password,
                                      my_name=self.client, remote_name=self.server,
                                      use_ntlm_v2=True, domain=self.domain, is_direct_tcp=True)
            self.connected = self.conn.connect(self.server_ip, self.port)
            return self.connected
        except Exception as s:
            print('error', s)
            return s

    def close(self):
        if self.connected:
            self.connected = False
            self.conn.close()
        else:
            raise Exception('Already not connected')

    def list_share(self):
        if self.connected:
            return [
                {
                    'Name': x.name,
                    'Type': x.type,
                    'IsTemporary': x.isTemporary,
                    'Comments': x.comments,
                } for x in self.conn.listShares() if not x.isSpecial
            ]
        else:
            return 'Not connected'

    def list_files(self, directory):
        files = []
        for item in self.conn.listPath(self.share, directory):
            files.append(item.filename)

        return files[2:]

    def sync_dir_over_smb(self, local_folder, smb_folder):
        try:
            self.connect()
        except Exception as s:
            print('smb_class_object not connected', s)
        for smb_file in self.list_files(smb_folder):
            if smb_file in os.listdir(local_folder):
                continue
            else:
                with open(os.path.join(local_folder, smb_file), 'wb') as fp:
                    self.conn.retrieveFile(self.share, os.path.join(smb_folder, smb_file), fp, timeout=30)
        if len(self.list_files(smb_folder)) == len(os.listdir(local_folder)):
            self.close()
            return True
        else:
            self.close()
            return False


def sync_file_logs():
    smb = Smb(LOGONS_USERNAME, LOGONS_PASSWORD, LOGONS_SERVER, LOGONS_LOGON_SHARE)
    return smb.sync_dir_over_smb(smb_folder=LOGONS_LOG_DIR, local_folder=LOGONS_LOCAL_LOG_DIR)
