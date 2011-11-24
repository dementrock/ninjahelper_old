import django.contrib.auth as auth
from django.shortcuts import redirect
from community.utils import login_ninjacourses
from common.utils import JsonResponse, JsonError, xrender
from django.core.context_processors import csrf

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
