from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from common.utils import JsonResponse, JsonError, xrender, redirecterror, JsonSuccess, ccnvalid
from django.shortcuts import redirect
from django.core.context_processors import csrf
from coursemonitor.models import CourseMonitor
from common.decorators import test_error

@test_error
@require_http_methods(['POST', ])
@login_required
def add_monitor_course(request):
    ccn = request.POST.get('ccn')
    if not ccnvalid(ccn):
        return JsonError('Invalid CCN.')
    user_profile = request.user.profile
    if CourseMonitor.objects.filter(user_profile=user_profile, ccn=int(ccn)).count():
        return JsonError('Already monitored this course.')
    CourseMonitor.objects.create(user_profile=user_profile, ccn=int(ccn))
    return JsonSuccess()
    
@test_error
@login_required
def manage_monitor_course(request):
    if not request.user.profile.is_contact_set:
        return redirecterror(request, 'You need to set up your cell phone or email first.')
    params = {}
    params.update(csrf(request))
    return xrender(request, 'manage_monitor_course.html', params)

@test_error
@login_required
def delete_monitor_course(request, ccn):
    user_profile = request.user.profile
    CourseMonitor.objects.filter(user_profile=user_profile, ccn=int(ccn)).delete()
    return redirect('manage_monitor_course')
