from community.models import UserProfile 
import django.contrib.auth as auth
from schedule.utils import fetch_page_after_auth
from django.core.urlresolvers import reverse

def login_ninjacourses(username, password):
    user = auth.authenticate(username=username, password=password)
    if user:
        return True
    try:
        result_page = fetch_page_after_auth(username=username, password=password, next_url='/')
    except Exception as e:
        print repr(e)
        return False
    UserProfile.get_or_create_user(username=username, password=password)
    return True
