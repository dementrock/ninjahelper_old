from django.contrib.auth.decorators import login_required
from common.utils import JsonResponse, JsonError, xrender, redirecterror
from community.models import MainScheduleCourse, CourseMonitor
from django.core.context_processors import csrf

@login_required
def set_phone(request):
    if request.method == 'POST':

    params = {}
    params.update(csrf(request))
    return xrender(request, 'set_phone.html', params)
