from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from community.utils import fetch_course_data, fetch_all_data, fetch_friend_data, fetch_compare_data, login_ninjacourses
from common.utils import JsonResponse, JsonError, ERROR_STATUS, SUCCESS_STATUS, xrender
from community.models import MainScheduleCourse, CourseMonitor
from django.contrib.auth.models import User
from django.core.context_processors import csrf
import hashlib

def login(request):
    try:
        if request.user.is_authenticated():
            return JsonError("Already logged in.")
        try:
            username = request.POST['username']
            password = request.POST['password']
        except Exception:
            return JsonError("Must provide both username and password.")
        if not username or not password:
            return JsonError("Must provide both username and password.")
        auth_successful = login_ninjacourses(username=username, password=password)
        print auth_successful
        if not auth_successful:
            return JsonError("We failed to authenticate your account on ninjacourses. Either the information is incorrect or the ninjacourses server is down.")
        print "getting user"
        print username, password
        user = auth.authenticate(username=username, password=password)
        print user
        print "logging in"
        auth.login(request, user)
        return JsonResponse(SUCCESS_STATUS)
    except Exception as e:
        print e
        return JsonError("Unknown error.")


def import_course_data(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return JsonResponse(ERROR_STATUS)
    try:
        return JsonResponse(fetch_course_data(username=username, password=password))
    except Exception as e:
        print e
        return JsonResponse(ERROR_STATUS)

def import_all_data(request):
    if not request.user.is_authenticated():
        return JsonError("Need to login first.")
    try:
        fetch_all_data(username=request.user.username, password=request.user.profile.ninjacourses_password)
    except Exception:
        return JsonError("Unknown error.")
    return JsonResponse(SUCCESS_STATUS)
    

def import_friend_data(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return JsonResponse(ERROR_STATUS)
    try:
        return JsonResponse(fetch_friend_data(username=username, password=password))
    except Exception as e:
        print e
        return JsonResponse(ERROR_STATUS) 

def compare_schedule(request):
    if not request.user.is_authenticated():
        return JsonError("Need to login first.")
    try:
        return JsonResponse(fetch_compare_data(username=request.user.username, password=request.user.profile.ninjacourses_password))
    except Exception:
        return JsonError("Unknown error.")

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return redirect('index')

def monitor_course(request):
    if request.method == 'POST':
        try:
            cellphone = request.POST['cellphone']
            ccn = request.POST['ccn']
            CourseMonitor.objects.create(user_profile=request.user.profile, ccn=int(ccn))
            params = {}
            params.update(csrf(request))
            params['ccn'] = ccn
            params['success'] = True
        except Exception as e:
            print e
            params = {}
            params.update(csrf(request))
            params['success'] = False
        return xrender(request, 'monitor_course_success.html', params)
    print "processing"
    try:
        params = {}
        params.update(csrf(request))
        params['course_list'] = request.user.profile.course_list
        return xrender(request, 'monitor_course.html', params)
    except Exception as e:
        print e
        return HttpResponse('fuck')

def add_monitor_course(request, course_ccn):
    user = request.user
    params = {}
    params.update(csrf(request))
    print user.profile.cellphone
    print MainScheduleCourse.objects.filter(course_ccn=course_ccn)
    course = MainScheduleCourse.objects.filter(course_ccn=course_ccn)[0]
    params['course'] = course
    if user.profile.cellphone == '0':
        return xrender(request, 'set_phone.html', params)
    return HttpResponse(str(course_ccn))
