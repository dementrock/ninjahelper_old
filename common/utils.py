from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson
import uuid
import urllib
import smtplib
import urlparse
import re

ERROR_STATUS = {'status': 'error'}
SUCCESS_STATUS = {'status': 'success'}

def generate_username():
    return uuid.uuid4().hex[0:30]

def generate_password():
    return uuid.uuid4().hex[0:16]

class JsonResponse(HttpResponse):
    def __init__(self, data):
        content = simplejson.dumps(data, indent=2, ensure_ascii=False)
        super(JsonResponse, self).__init__(content=content)

class JsonError(JsonResponse):
    def __init__(self, error_msg):
        data = ERROR_STATUS
        data['message'] = error_msg
        super(JsonError, self).__init__(data=data)

class JsonSuccess(JsonResponse):
    def __init__(self, msg=''):
        data = SUCCESS_STATUS
        data['message'] = msg
        super(JsonSuccess, self).__init__(data=data)

def xrender(request, template_url, args):
    args['request'] = request
    return render_to_response(template_url, args)

def redirecterror(request, msg=''):
    return xrender(request, 'error.html', {'msg': msg})

def urlvalid(url):
    return url.startswith('http://') or url.startswith('https://')
    """url_re = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    match_list = url_re.findall(url)
    print "Validating url", match_list
    return len(match_list) == 1 and match_list[0] == url"""

def send_message(toaddrs='peterqian1993@hotmail.com', msg='nothing'):
    print toaddrs, msg
    from settings import EMAIL_SENDER_ADDRS, EMAIL_SENDER_PASSWORD
    fromaddr = EMAIL_SENDER_ADDRS
    # Credentials (if needed)  
    username = EMAIL_SENDER_ADDRS
    password = EMAIL_SENDER_PASSWORD

    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    print "Sending..."
    server.sendmail(fromaddr, toaddrs, msg)  
    print "Message sent"
    server.quit() 
