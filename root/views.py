from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from common.utils import xrender
from mechanize import Browser
import hashlib

def index(request):
    params = {}
    params.update(csrf(request))
    if request.user.is_authenticated():
        return xrender(request, 'index.html', params)
    else:
        return xrender(request, 'login.html', params)

def test(request):
    url = 'http://ninjacourses.com'
    br = Browser()
    br.set_handle_robots(False)
    br.open(url)
    print br.response()
    print br
    return HttpResponse(br.read())
