from django.shortcuts import render
from django.views.decorators.http import require_GET
import datetime
from acs_logs.models import show_vpn_logon, sync_file_logs, import_logs_into_db


@require_GET
def acs_search(request):
    """

    :param request:
        input_search: Search string
        type_search: Type of search from specified (login, last_logon, full_name)
    :return:
    """
    try:
        input_search = request.GET['input_search']
        type_search = request.GET['type_search']
    except:
        input_search = ''
        type_search = 'login'

    try:
        xrange = request.GET['xrange']
    except:
        # Default interval search - 30 last days
        xrange = {
            "start": datetime.datetime.today().date().__str__(),
            "end": (datetime.datetime.today() - datetime.timedelta(days=30)).date().__str__(),
        }

    #sync_file_logs()
    #import_logs_into_db()

    if input_search == '':
        return render(request, 'portal/acs-search.html', {
            'title': 'ACS Search', })
    else:
        acs = show_vpn_logon(input_search, type_search)
        print(acs)
        if type_search == 'login':
            content = {'title': 'ACS search in log files',
                       'rowName': 'Vpn user logged on',
                       'colName': ['time','user_name', 'group_name', 'acct_status_type',
                                   'acct_session_time', 'acct_input_octets', 'acct_output_octets'],
                       'data': acs,
                       }
            return render(request, 'portal/acs-search.html', content)

        elif type_search == 'last_logon':
            content = {'title': 'ACS search in log files',
                       'rowName': 'Vpn user logged on ',
                       'colName': acs,
                       }
            return render(request, 'portal/acs-search.html', content)
