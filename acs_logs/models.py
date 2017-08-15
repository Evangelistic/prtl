from django.db import models
from portal.settings import ACS_USERNAME, ACS_PASSWORD, ACS_SERVER, ACS_LOG_DIR, LOCAL_LOG_DIR, ACS_SHARE
import socket
import os
import datetime
import csv
from smb.SMBConnection import SMBConnection
import logging
from modify_ad_data.models import search_in_ad


class ACSLogF(models.Model):
    acs_log_file = models.CharField(max_length=128, unique=True)
    acs_log_data = models.DateField(default=None, db_index=True)

    def __str__(self):
        return dict(
            acs_log_file=self.acs_log_file,
            acs_log_data=self.acs_log_data,
        ).__str__()

    class Meta:
        ordering = ['-acs_log_data']


class ACSLog(models.Model):
    time = models.TimeField()
    user_name = models.CharField(max_length=64, db_index=True)
    group_name = models.CharField(max_length=128)
    acct_status_type = models.CharField(max_length=128)
    acct_session_time = models.IntegerField(default=0)
    acct_input_octets = models.CharField(max_length=64, blank=True)
    acct_output_octets = models.CharField(max_length=64, blank=True)

    acs_log_file = models.ForeignKey(ACSLogF, on_delete=models.CASCADE)

    def __str__(self):
        return dict(
            time=self.time,
            user_name=self.user_name,
            group_name=self.group_name,
            acct_status_type=self.acct_status_type,
            acct_session_time=self.acct_session_time,
            acct_input_octets=self.acct_input_octets,
            acct_output_octets=self.acct_output_octets
        ).__str__()


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
    smb = Smb(ACS_USERNAME, ACS_PASSWORD, ACS_SERVER, ACS_SHARE)
    smb.sync_dir_over_smb(smb_folder=ACS_LOG_DIR, local_folder=LOCAL_LOG_DIR)


def import_logs_into_db():

    local_logs = []
    # Проверка на наличие записи о файлен в базе
    for log_file in os.listdir(LOCAL_LOG_DIR):
        try:
            acs_f = ACSLogF.objects.get(acs_log_file=log_file)
        except ACSLogF.DoesNotExist:
            acs_f = None
        if not acs_f:
            local_logs.append(log_file)

    # Итерируемся по отсутствующим файлам
    for csvfile in local_logs:
        print(csvfile)
        lf = ACSLogF.objects.create(
            acs_log_data=datetime.datetime.strptime(csvfile[18:-4], '%Y-%m-%d'),
            acs_log_file=csvfile)

        with open(os.path.join(LOCAL_LOG_DIR, csvfile), encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:

                if row['Acct-Session-Time'] == '':
                    row['Acct-Session-Time'] = 0

                lr = ACSLog.objects.create(
                    acs_log_file=lf,
                    time=row['Time'],
                    user_name=row['User-Name'],
                    group_name=row['Group-Name'],
                    acct_status_type=row['Acct-Status-Type'],
                    acct_session_time=row['Acct-Session-Time'],
                    acct_input_octets=row['Acct-Input-Octets'],
                    acct_output_octets=row['Acct-Output-Octets']
                )


def show_vpn_logon(input_search, type_search):

    if type_search == 'full_name':
        input_search = search_in_ad(
            type_object='Person',
            type_search='cn',
            who_is=input_search)[0]['attributes']['sAMAccountName']
    print(input_search)
    try:
        acs = ACSLog.objects
        acs = acs.filter(user_name=input_search)
        acs = acs
    except ACSLogF.DoesNotExist:
        acs = None

    response = []
    for i in acs:
        temp = {
            'time': i.time.isoformat(),
            'user_name': i.user_name,
            'group_name': i.group_name,
            'acct_status_type': i.acct_status_type,
            'acct_session_time': i.acct_session_time,
            'acct_input_octets': i.acct_input_octets,
            'acct_output_octets': i.acct_output_octets
        }
        response.append(temp)
    return response
