from django.shortcuts import render
from .models import search_in_ad, modify_in_ad


# from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
# Create your views here.

AD_ATTRIBUTE = {
    'full_name': 'cn',
    'email': 'mail',
}


def ad_modify(request):
    """
    Request example:    type_search (full_name, email) - AD-attribute that we change
                        input_search (sAMAccountName new_value_attr) - AD-object that we change and new value attribute
    :param request:
    typeSearch: full_name, email
    input_search: sAMAccountName new_value_attr
    :return:
    """
    new_value_attr = None

    try:
        who_is = request.POST['input_search'].split()[0]
        new_value_attr = ' '.join(request.POST['input_search'].split()[1:])
        type_attribute = AD_ATTRIBUTE[request.POST['type_search']]
    except:
        who_is = ''
        type_attribute = 'full_name'
    if who_is == '':
        return render(request, 'portal/ad-modify.html', {
            'title': 'AD Modify', })
    else:
        type_object = r'Person'
        search_who_is = r'sAMAccountName'
        data_dn = search_in_ad(type_object, search_who_is, who_is)[0]['attributes']
        data_old = data_dn

        if new_value_attr:
            modify_in_ad(data_dn, type_attribute, new_value_attr)
        else:
            print("FAIL")

        data_new = search_in_ad(type_object, search_who_is, who_is)[0]['attributes']

        content = {'title': 'AD Modify',
                   'row_name': 'Processed data',
                   'col_name': [i for i in data_dn],
                   'status': ['old', 'new'],
                   'data_new': data_new,
                   'data_old': data_old,
                   }

        return render(request, 'portal/ad-modify.html', content)
