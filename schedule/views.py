# Create your views here.

from django.contrib.auth.decorators import login_required
from schedule.utils import fetch_all_data, fetch_compare_data, get_friend_expression
from common.utils import JsonResponse, JsonError, JsonSuccess, xrender, redirecterror
from django.core.context_processors import csrf

def import_all_data(request):
    if not request.user.is_authenticated():
        return JsonError("Need to login first.")
    try:
        fetch_all_data(username=request.user.username, password=request.user.profile.ninjacourses_password)
    except Exception as e:
        print repr(e)
        return JsonError('Unknown error.')
    return JsonSuccess('Your data is imported.')
    
@login_required
def compare_schedule(request):
    try:
        cmp_data = fetch_compare_data(username=request.user.username, password=request.user.profile.ninjacourses_password)
        cmp_result = '<div class="form-header">According to your friend list, you will attend...</div><div class="comparelist">';
        for course_name, friend_list in cmp_data:
            cmp_result += '<div class="compareitem"><span class="coursename">%s</span> with %s.</div>' % (course_name, get_friend_expression(friend_list))
        cmp_result += '</div>'
        return xrender(request, 'compare_schedule.html', {'cmp_result': cmp_result})
    except Exception as e:
        print repr(e)
        return redirecterror(request, 'Unknown error.')

def get_friend_expression(friend_list):
    friend_str = ""
    cnt_friend = len(friend_list)
    if not cnt_friend:
        friend_str = '<span class="noneofyourfriends">none of your friends</span>'
    else:
        for i in range(0, cnt_friend):
            friend = friend_list[i]
            if i == cnt_friend - 1 and cnt_friend > 1:
                if cnt_friend > 2:
                    friend_str += 'and '
                else:
                    friend_str += ' and '
            friend_str += '<a href="http://ninjacourses.com%s">%s</a>' % (friend[1], friend[0])
            if (i < cnt_friend - 1):
                if cnt_friend > 2:
                    friend_str += ', '
    return friend_str
