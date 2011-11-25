from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from common.utils import JsonResponse, JsonError, JsonSuccess, xrender, redirecterror
from community.models import UserProfile
from community.utils import emailvalid, send_email_verification
from django.core.context_processors import csrf

@login_required
def set_email(request):
    if request.user.profile.is_email_set:
        return redirecterror(request, 'Your email is already set.')
    if request.method == 'POST':
        try:
            if 'type' not in request.POST or request.POST['type'] not in ['get_random_code', 'submit', ]:
                return JsonError('Invalid request.')
            if request.POST['type'] == 'get_random_code':
                if 'email' not in request.POST or not request.POST['email']:
                    return JsonError('Must provide email address.')
                email = request.POST['email']
                if not emailvalid(email):
                    return JsonError('Invalid email address.')
                send_email_verification(request, email)
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
                del request.session['code_dict']
                del request.session['cellphone']
                return JsonSuccess('Your phone is set up.')
        except Exception as e:
            print repr(e)
            return JsonError('Unknown error.')
    else:
        params = {}
        params.update(csrf(request))
        return xrender(request, 'set_email.html', params)

def verify_email(request, code):
    try:
        print code
        print request.user.profile.email_verification_code
        UserProfile.objects.get(email_verification_code=code).set_email()
        return redirect('index')
    except Exception as e:
        print repr(e)
        return redirecterror(request, 'Invalid verification code.')
