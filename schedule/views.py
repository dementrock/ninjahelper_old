# Create your views here.

from django.contrib.auth.decorators import login_required
from schedule.utils import fetch_all_data, fetch_compare_data, get_friend_expression
from common.utils import JsonResponse, JsonError, JsonSuccess, xrender, redirecterror
from django.core.context_processors import csrf
from common.decorators import test_error

@test_error
def import_all_data(request):
    if not request.user.is_authenticated():
        return JsonError("Need to login first.")
    fetch_all_data(request.user.profile)
    return JsonSuccess('Your data is imported.')
    
@test_error
@login_required
def compare_schedule(request):
    cmp_data = fetch_compare_data(request.user.profile)
    cmp_result = '<div class="form-header">According to your friend list, you will attend...</div><div class="comparelist">';
    for course_name, friend_list in cmp_data:
        cmp_result += '<div class="compareitem"><span class="coursename">%s</span> with %s.</div>' % (course_name, get_friend_expression(friend_list))
    cmp_result += '</div>'
    return xrender(request, 'compare_schedule.html', {'cmp_result': cmp_result})
