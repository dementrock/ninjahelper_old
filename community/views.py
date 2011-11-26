import django.contrib.auth as auth
from django.shortcuts import redirect
from community.utils import login_ninjacourses
from common.utils import JsonResponse, JsonError, JsonSuccess, xrender, emailvalid, cellphonevalid, send_random_code, send_email_verification
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

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
            return JsonSuccess()
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

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return redirect('index')

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
                if randomcode == request.user.profile.email_short_code:
                    request.user.profile.set_email()
                    return JsonSuccess('Your email is set up.')
                else:
                    return JsonError('Incorrect code.')
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
                del request.session['code_dict']
                del request.session['cellphone']
                return JsonSuccess('Your phone is set up.')
        except Exception as e:
            print repr(e)
            return JsonError('Unknown error.')
    else:
        params = {}
        params['cellphone'] = request.session.get('cellphone', '')
        params.update(csrf(request))
        return xrender(request, 'set_phone.html', params)
