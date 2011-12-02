from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson
from mechanize import Browser
import uuid
import urllib
import smtplib
import urlparse
import re
import string
import random
from django.core.urlresolvers import reverse
from settings import MEDIA_HEADER

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
    args['media_header'] = MEDIA_HEADER
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

def send_email(toaddrs, title, msg):
    from email.mime.text import MIMEText
    from settings import EMAIL_SENDER_ADDRS
    msg = MIMEText(msg, 'html')
    msg['Subject'] = title
    msg['From'] = EMAIL_SENDER_ADDRS
    msg['To'] = toaddrs
    send_message(toaddrs, msg.as_string())

def getsize(url):
    import urllib
    try:
        return int(urllib.urlopen(url).info().getheaders('Content-Length')[0])
    except Exception as e:
        print repr(e)
        raise ValueError

def gethash(url):
    import urllib
    import md5
    content = urllib.urlopen(url).read()
    md5_handler = md5.new()
    md5_handler.update(content)
    return md5_handler.hexdigest()

def cellphonevalid(phonenumber):
    return phonenumber.isdigit() and len(phonenumber) == 10

def ccnvalid(ccn):
    return ccn and ccn.isdigit() and len(ccn) == 5

_cell_mail_list = [
    #'message.alltel.com',
    'txt.att.net',
    #'myboostmobile.com',
    #'messaging.nextel.com',
    #'messaging.sprintpcs.com',
    'tmomail.net',
    #'email.uscc.net',
    'vtext.com',
    #'vmobl.com',
]

RANDOM_CODE = string.digits + string.letters

def get_random_code(length=4):
    return "".join([random.choice(RANDOM_CODE) for _ in range(length)])

def send_random_code(request, cellphone):
    request.session['code_dict'] = {'0': 'fuck'}
    for cell_mail in _cell_mail_list:
        random_code = '0'
        while request.session['code_dict'].get(random_code):
            random_code = get_random_code()
        request.session['code_dict'][random_code] = cell_mail
        complete_cell_mail = "{0}@{1}".format(cellphone, cell_mail)
        send_message(toaddrs=complete_cell_mail, msg=random_code)

def emailvalid(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def send_email_verification(request, email):

    from settings import WEBSITE_URL
    from urlparse import urljoin

    shortcode = get_random_code()
    emailcode = uuid.uuid4().hex

    profile = request.user.profile
    profile.email_to_verify = email
    profile.email_short_code = shortcode
    profile.email_verification_code = emailcode
    profile.save()

    url = urljoin(WEBSITE_URL, reverse('verify_email', args=[emailcode, ]))
    send_email(toaddrs=email, title='Email verification code from Ninja Helper', msg="This email is sent from Ninja Helper to verify your email address. The verification code is <b>%s</b>, or you can click the link below:<br />%s" % (shortcode, url), )

def errorlog(e, function=None):
    from settings import DEBUG
    error_str = 'Error %s in function %s' % (repr(e), str(function) if function else '(unprovided)')
    if DEBUG:
        print (error_str)
    else:
        open('error_log', 'a').write(error_str)
