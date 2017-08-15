from django.shortcuts import render
from django.views.decorators.http import require_POST
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from portal.settings import EMAIL_USER_NAME, EMAIL_PASSWORD, EMAIL_DEFAULT_LIST, COMPANY_MAP, COMPANY_INFO


@require_POST
def send(request):
    name = request.POST['name']
    email_subject = request.POST['email_subject']
    reply_email = request.POST['reply_email']
    phone = request.POST['phone']
    company_name = request.POST['company_name']
    email_msg = request.POST['email_msg'].replace('\n', '<br />')
    res = send_email(name, email_subject, reply_email, phone, company_name, email_msg)
    if res == 0:
        content = {
            'title': 'Security contacts',
            'company_map': COMPANY_MAP,
            'company_info': COMPANY_INFO,
            'result': 'Ваше сообщение отправлено.'
        }
    else:
        content = {
            'title': 'Security contacts',
            'company_map': COMPANY_MAP,
            'company_info': COMPANY_INFO,
            'result': 'При отправке произошла ошибка. Попробуйте позже.'
        }
    return render(request, 'portal/contact-us.html', content)


def send_email(name, email_subject, reply_email, phone, company_name, email_msg, toaddrs=EMAIL_DEFAULT_LIST):
    try:
        fromaddr = "security portal"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER_NAME, EMAIL_PASSWORD)
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(toaddrs)
        msg['Subject'] = email_subject
        body = "<p>Ahtung,  nicht arbeiten!!!</p><br>\
        Name: " + name + "<br>\
        Reply_email: " + reply_email + "<br>\
        Phone: " + phone + "<br>\
        Company_name: " + company_name + "<br><br>\
        Text: " + email_msg + "<br>\
        "
        msg.attach(MIMEText(body, _subtype='html'))
        text = msg.as_string()
        server.sendmail(fromaddr, toaddrs, text)
        server.quit()
        return 0
    except SystemError:
        return 1
