from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from common.utils import JsonResponse, JsonError, xrender, redirecterror, JsonSuccess, urlvalid
from django.shortcuts import redirect
from community.models import CoursePageMonitor
from community.utils import ccnvalid
from django.core.context_processors import csrf

@require_http_methods(['POST', ])
@login_required
def add_monitor_course_page(request):
    try:
        url = request.POST.get('url')
        if not urlvalid(url):
            return JsonError('Invalid url.')
        user_profile = request.user.profile
        if CoursePageMonitor.objects.filter(user_profile=user_profile, url=url).count():
            return JsonError('Already monitored this page.')
        CoursePageMonitor.objects.create(user_profile=user_profile, url=url)
        return JsonSuccess()
    except Exception as e:
        print repr(e)
        return JsonError('Unknown error.')
    

@login_required
def manage_monitor_course_page(request):
    if not request.user.profile.is_email_set:
        return redirecterror(request, 'You need to set up your email first.')
    try:
        params = {}
        params.update(csrf(request))
        return xrender(request, 'manage_monitor_course_page.html', params)
    except Exception as e:
        print repr(e)
        return redirecterror(request, 'Unknown error.')

@login_required
def delete_monitor_course_page(request, course_page_id):
    CoursePageMonitor.objects.filter(user_profile=request.user.profile, id=course_page_id).delete()
    return redirect('manage_monitor_course_page')
