from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
import root.views
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from community.utils import fetch_course_data, fetch_all_data, fetch_friend_data, fetch_compare_data, login_ninjacourses
from common.utils import JsonResponse, JsonError, ERROR_STATUS, SUCCESS_STATUS, xrender, redirecterror
from community.models import MainScheduleCourse, CourseMonitor, ShortLink
from django.contrib.auth.models import User
from django.core.context_processors import csrf
import hashlib
from community.forms import ShortLinkForm

def import_all_data(request):
    if not request.user.is_authenticated():
        return JsonError("Need to login first.")
    try:
        fetch_all_data(username=request.user.username, password=request.user.profile.ninjacourses_password)
    except Exception as e:
        return JsonError("Unhandled error: %s" % str(e))
    return JsonResponse(SUCCESS_STATUS)
    
@login_required
def compare_schedule(request):
    if not request.user.is_authenticated():
        return JsonError("Need to login first.")
    try:
        return JsonResponse(fetch_compare_data(username=request.user.username, password=request.user.profile.ninjacourses_password))
    except Exception:
        return JsonError("Unknown error.")
