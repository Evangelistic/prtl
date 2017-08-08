from django.shortcuts import render
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Create your views here.

def send_mail(name,email_subject,reply_email,phone,company_name,email_msg,toaddrs = ["aderevyankin@willesden.by","vvlasenko@willesden.by"]):
    fromaddr = "security portal"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('bwd.reports@gmail.com', ',fhf,firf2017')
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddrs)
    msg['Subject'] = email_subject
    body = "<p>Ahtung,  nicht arbeiten!!!</p><br>\
    Name: "+ name +"<br>\
    Reply_email: " + reply_email + "<br>\
    Phone: " + phone + "<br>\
    Company_name: " + company_name + "<br><br>\
    Text: " + email_msg + "<br>\
    "
    msg.attach(MIMEText(body, _charset='koi8-r', _subtype='html'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddrs, text)
    server.quit()
    return 0
