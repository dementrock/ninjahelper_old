from django.contrib.auth.decorators import login_required
from common.utils import JsonResponse, JsonError, xrender, redirecterror
from community.models import MainScheduleCourse, CourseMonitor
from django.core.context_processors import csrf

@login_required
def manage_monitor_course(request):
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
        print repr(e)
        return redirecterror(request, 'Unknown error.')
