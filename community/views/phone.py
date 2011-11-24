from django.contrib.auth.decorators import login_required
from common.utils import JsonResponse, JsonError, JsonSuccess, xrender, redirecterror
from community.models import MainScheduleCourse, CourseMonitor
from community.utils import cellphonevalid, send_random_code
from django.core.context_processors import csrf
from django.views.decorators.http import require_http_methods

@login_required
def set_phone(request):
    if request.user.profile.is_phone_set:
        return redirecterror(request, 'Your phone is already set.')
    if request.method == 'POST':
        try:
            if 'type' not in request.POST or request.POST['type'] not in ['get_random_code', 'submit', ]:
                return JsonError('Invalid request.')
            if request.POST['type'] == 'get_random_code':
                if 'cellphone' not in request.POST or not request.POST['cellphone']:
                    return JsonError('Must provide cell phone number.')
                cellphone = request.POST['cellphone']
                if not cellphonevalid(cellphone):
                    return JsonError('Cell phone format incorrect: must be 10 digit number without slashes.')
                request.session['cellphone'] = cellphone
                send_random_code(request, cellphone)
                return JsonSuccess('Random code sent.')
            else:
                if 'randomcode' not in request.POST or not request.POST['randomcode']:
                    return JsonError('Must provide randomcode.')
                randomcode = request.POST['randomcode']
                cellphone = request.session.get('cellphone')
                code_dict = request.session.get('code_dict')
                if not cellphone or not code_dict:
                    return JsonError('Phone number not found. Please retype your phone number and submit again.')
                cell_mail = code_dict.get(randomcode)
                if not cell_mail:
                    return JsonError('Code incorrect or we do not support your phone service.')
                request.user.profile.set_phone(cellphone, cell_mail)
                return JsonSuccess('Your phone is set up.')
        except Exception as e:
            print repr(e)
            return JsonError('Unknown error.')
    else:
        params = {}
        params['cellphone'] = request.session.get('cellphone', '')
        params.update(csrf(request))
        return xrender(request, 'set_phone.html', params)
