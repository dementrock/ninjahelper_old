import sys
import json
import re
import string
import random
import uuid
from mechanize import ParseResponse, urlopen, urljoin, Browser
from django.contrib.auth.models import User
from community.models import UserProfile 
import django.contrib.auth as auth
from common.utils import send_message
from django.core.urlresolvers import reverse

class ResponseWrapper(object):
    filter_rules = {'<div class="form_div">': '',
            '<label for="id_username">Username or email</label><br/>': '',
            '<label for="id_password">Password</label><br/>': '',
            '<div class="help-text"></div></div>': '<div class="help-text"></div>', }
    def __init__(self, raw_response):
        self._content = raw_response.read()
        for pre_filter, post_filter in self.filter_rules.items():
            self._content = self._content.replace(pre_filter, post_filter)
        self._url = raw_response.geturl()
        self._pointer = 0
    def read(self, max_length=0):
        pointer = self._pointer
        if not max_length:
            self._pointer = len(self._content)
            return self._content[pointer:]
        else:
            self._pointer += max_length
            return self._content[pointer:pointer+max_length]
    def geturl(self):
        return self._url

def login_ninjacourses(username, password):
    user = auth.authenticate(username=username, password=password)
    if user:
        return True
    try:
        result_page = _fetch_page_after_auth(username=username, password=password, next_url='/')
    except Exception:
        return False
    UserProfile.get_or_create_user(username=username, password=password)
    return True

def _fetch_page_after_auth(username, password, next_url):
    logout_url = 'https://secure.ninjacourses.com/account/logout/'
    login_url = 'https://secure.ninjacourses.com/account/login/?next=%s' % next_url
    br = Browser(file_wrapper=ResponseWrapper)
    br.set_handle_robots(False)
    br.open(logout_url)
    br.open(login_url)
    br.select_form()
    br['username'], br['password'] = username, password
    result_page = br.submit().read()
    br.close()
    if 'correct username' in result_page:
        raise ValueError
    return result_page


def _fetch_user_schedule_page(username, password):
    return _fetch_page_after_auth(username, password, '/schedule/view/')
    
def _fetch_user_friend_list_page(username, password):
    return _fetch_page_after_auth(username, password, '/friends/')

def _fetch_friend_schedule_page(url, username, password):
    return _fetch_page_after_auth(username, password, url)

def _get_from_schedule(schedule, item_name):
        try:
            return json.loads(re.search('%s = (.*);' % item_name, schedule).group(1))
        except Exception:
            return None

def _fetch_course_data_from_page(page):

    print 'Start parsing...'
    try:
        main_schedule_entries = _get_from_schedule(page, 'view.schedules_entries')[0] # Only interested in the main schedule
    except Exception:
        print "Error when fetching main schedule entries"
        return None
    try:
        offerings = _get_from_schedule(page, 'view.offerings')
    except Exception as e:
        print e

    course_list = []

    for section in main_schedule_entries['sections']:
        if not section['offering_id']:
            continue
        try:
            course_ccn = int(section['data']['ccn'])
        except Exception:
            course_ccn = 0
        try:
            offering = offerings[str(section['offering_id'])]
            friendly_name = ''
            if offering['course']['department']['shorthand']:
                friendly_name += offering['course']['department']['shorthand']
            else:
                friendly_name += offering['course']['department']['code']
            friendly_name += ' ' + offering['course']['identifier'] + ' ' + section['data']['friendly_name']
            course_id = offering['course']['id']
            course_list.append([friendly_name, course_id, course_ccn])
        except Exception as e:
            print e
            continue
    return course_list

def _fetch_friend_list_from_page(page):
    friend_list = []
    from lxml.html import fromstring
    li_list = fromstring(page).cssselect('.friends-list>li')
    for li in li_list:
        try:
            username = li.cssselect('strong')[0].text_content()
        except Exception:
            continue
        try:
            name = li.cssselect('i')[0].text_content()
        except Exception as e:
            name = ''
        try:
            friend_url =  li.cssselect('a')[0].get('href')
        except Exception as e:
            friend_url = ''
        friend_list.append([username, name, friend_url])
    print friend_list
    return friend_list

def _get_course_list(user_profile, username, password):
    print 'Processing friend %s' % str(user_profile)
    if user_profile.is_main_schedule_imported:
        return user_profile.course_list
    print 'Fetching page..'
    friend_schedule_page = _fetch_friend_schedule_page(url=user_profile.url_as_friend, username=username, password=password)
    print 'Parsing course list...'
    course_list = _fetch_course_data_from_page(friend_schedule_page)
    print 'Saving result..'
    user_profile.set_main_schedule(course_list)
    return course_list


def fetch_course_data(username, password):
    user, user_profile = UserProfile.get_or_create_user(username=username, password=password)
    if user_profile.is_main_schedule_imported:
        return user_profile.course_list
    user_schedule_page = _fetch_user_schedule_page(username, password)
    course_list = _fetch_course_data_from_page(user_schedule_page)
    print "Fetched course list"
    print course_list
    user_profile.set_main_schedule(course_list)
    return course_list
    
def fetch_friend_data(username, password):
    print "Fetching friend %s, %s" % (username, password)
    user, user_profile = UserProfile.get_or_create_user(username=username, password=password)
    if user_profile.is_friend_list_imported:
        return user_profile.friend_list
    friend_list_page = _fetch_user_friend_list_page(username, password)
    friend_list = _fetch_friend_list_from_page(friend_list_page)
    user_profile.set_friend_list(friend_list)
    return friend_list 

def fetch_all_data(username, password):
    print username, password
    user, user_profile = UserProfile.get_or_create_user(username=username, password=password)
    print user, user_profile
    if not user_profile.is_main_schedule_imported:
        course_list = fetch_course_data(username, password)
        user_profile.set_main_schedule_imported()
    print "Fetched course data"
    if not user_profile.is_friend_list_imported:
        print "Fetching friend data"
        fetch_friend_data(username, password)
        user_profile.set_friend_list_imported()
    if not user_profile.is_friend_schedule_imported:
        for friend_profile in user_profile.friend.all():
            _get_course_list(user_profile=friend_profile, username=username, password=password)
        user_profile.set_friend_schedule_imported()

def fetch_compare_data(username, password):

    compare_dict = {}
    
    user, user_profile = UserProfile.get_or_create_user(username=username, password=password)

    if not user_profile.is_main_schedule_imported:
        print "Need to import main schedule"
        fetch_course_data(username, password)
        print "Import finished"
    course_list = user_profile.course_list
    if not user_profile.is_friend_list_imported:
        fetch_friend_data(username, password)
    friend_list = [[str(x), x.url_as_friend, _get_course_list(user_profile=x, username=username, password=password)] for x in user_profile.friend.all() if x != user_profile]

    for friendly_name, course_id in course_list:
        compare_dict[friendly_name] = []

    for friend_name, friend_url, friend_course_list in friend_list:
        print friend_name, friend_url, friend_course_list
        if type(friend_course_list) is list:
            for friendly_name, course_id in friend_course_list:
                if friendly_name in compare_dict:
                    compare_dict[friendly_name].append([friend_name, friend_url])

    return compare_dict.items()

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

def get_friend_expression(friend_list):
    friend_str = ""
    cnt_friend = len(friend_list)
    if not cnt_friend:
        friend_str = '<span class="noneofyourfriends">none of your friends</span>'
    else:
        for i in range(0, cnt_friend):
            friend = friend_list[i]
            if i == cnt_friend - 1 and cnt_friend > 1:
                if cnt_friend > 2:
                    friend_str += 'and '
                else:
                    friend_str += ' and '
            friend_str += '<a href="http://ninjacourses.com%s">%s</a>' % (friend[1], friend[0])
            if (i < cnt_friend - 1):
                if cnt_friend > 2:
                    friend_str += ', '
    return friend_str

def emailvalid(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def send_email_verification(request, email):

    from settings import EMAIL_SENDER_ADDRS
    from email.mime.text import MIMEText

    shortcode = get_random_code()
    emailcode = uuid.uuid4().hex

    profile = request.user.profile
    profile.email_to_verify = email
    profile.email_short_code = shortcode
    profile.email_verification_code = emailcode
    profile.save()

    url = 'http://ninjahelper.com' + reverse('verify_email', args=[emailcode, ])
    msg = MIMEText("This email is sent from Ninja Helper to verify your email address. The verification code is <strong>%s</strong>, or you can click the link below:<br /> %s" % (shortcode, url))
    msg['Subject'] = 'Email verification code from Ninja Helper'
    msg['From'] = EMAIL_SENDER_ADDRS
    msg['To'] = email
    print msg.as_string()
    send_message(email, msg.as_string()) 
