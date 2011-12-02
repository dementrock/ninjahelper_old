# Create your views here.

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from common.utils import JsonResponse, JsonError, xrender, redirecterror, JsonSuccess, urlvalid, getsize, ccnvalid
from coursepagemonitor.models import CoursePageMonitor
from django.shortcuts import redirect
from settings import MAXIMUM_SIZE
from django.core.context_processors import csrf
from common.decorators import test_error

@test_error
@require_http_methods(['POST', ])
@login_required
def add_monitor_course_page(request):
    if 'url' not in request.POST or not request.POST['url'] or 'shortname' not in request.POST or not request.POST['shortname']:
        return JsonError('Must provide both URL and short name.')
    url, shortname = request.POST['url'], request.POST['shortname']
    if not urlvalid(url):
        return JsonError('Invalid URL.')
    user_profile = request.user.profile
    if CoursePageMonitor.objects.filter(user_profile=user_profile, shortname=shortname).count():
        return JsonError('Short name already in use.')
    if CoursePageMonitor.objects.filter(user_profile=user_profile, url=url).count():
        return JsonError('Already monitored this page.')
    try:
        if getsize(url) > MAXIMUM_SIZE:
            return JsonError('Page too large')
    except ValueError:
        return JsonError('Cannot access url or we cannot determine the file size.')
    CoursePageMonitor.objects.create(user_profile=user_profile, url=url, shortname=shortname)
    return JsonSuccess()
    
@test_error
@login_required
def manage_monitor_course_page(request):
    if not request.user.profile.is_email_set:
        return redirecterror(request, 'You need to set up your email first.')
    params = {}
    params.update(csrf(request))
    return xrender(request, 'manage_monitor_course_page.html', params)

@test_error
@login_required
def delete_monitor_course_page(request, shortname):
    CoursePageMonitor.objects.filter(user_profile=request.user.profile, shortname=shortname).delete()
    return redirect('manage_monitor_course_page')
