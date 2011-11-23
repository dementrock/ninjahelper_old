from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
import root.views
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from community.utils import fetch_course_data, fetch_all_data, fetch_friend_data, fetch_compare_data, login_ninjacourses
from common.utils import JsonResponse, JsonError, ERROR_STATUS, SUCCESS_STATUS, xrender
from community.models import MainScheduleCourse, CourseMonitor, ShortLink
from django.contrib.auth.models import User
from django.core.context_processors import csrf
import hashlib

def login(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated():
                return JsonError("Already logged in.")
            try:
                username = request.POST['username'].lower()
                password = request.POST['password']
            except Exception:
                return JsonError("Must provide both username and password.")
            if not username or not password:
                return JsonError("Must provide both username and password.")
            if '@' in username:
                return JsonError("Please use your username instead of email address.")
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
    else:
        params = {}
        try:
            params['next'] = request.GET['next']
        except Exception:
            params['next'] = '/'
        params.update(csrf(request))
        if request.user.is_authenticated():
            return redirect('index')
        else:
            return xrender(request, 'login.html', params)


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
    except Exception as e:
        return JsonError("Unhandled error: %s" % str(e))
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

@login_required
def compare_schedule(request):
    if not request.user.is_authenticated():
        return JsonError("Need to login first.")
    try:
        return JsonResponse(fetch_compare_data(username=request.user.username, password=request.user.profile.ninjacourses_password))
    except Exception:
        return JsonError("Unknown error.")

@login_required
def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return redirect('index')

@login_required
def monitor_course(request):
    if request.method == 'POST':
        try:
            cellphone = request.POST['cellphone']
            ccn = request.POST['ccn']
            user_profile = request.user.profile
            user_profile.set_phone(cellphone)
            CourseMonitor.objects.create(user_profile=user_profile, ccn=int(ccn))
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

@login_required
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

@login_required
def manage_shortlink(request):
    params = {}
    params.update(csrf(request))
    return xrender(request, 'manage_shortlink.html', params)


@login_required
def add_shortlink(request):
    try:
        shortname = request.POST['shortname']
        url = request.POST['url']
        user_profile = request.user.profile
        ShortLink.objects.create(shortname=shortname, url=url, user_profile=user_profile)
        return JsonResponse(SUCCESS_STATUS)
    except Exception as e:
        print e
        return JsonError('Unknown error')

@login_required
def shortlink(request, shortname):
    try:
        linkobj = ShortLink.objects.get(user_profile=request.user.profile, shortname=shortname)
        return redirect(linkobj.url)
    except Exception as e:
        print e
        return redirect('error')


@login_required
def edit_shortlink(request, shortname):
    try:
        linkobj = ShortLink.objects.get(user_profile=request.user.profile, shortname=shortname)
        return redirect(linkobj.url)
    except Exception as e:
        print e
        return redirect('index')

@login_required
def delete_shortlink(request, shortname):
    try:
        linkobj = ShortLink.objects.get(user_profile=request.user.profile, shortname=shortname)
        return redirect(linkobj.url)
    except Exception as e:
        print e
        return redirect('index')
