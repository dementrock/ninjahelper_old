from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from common.utils import JsonResponse, JsonError, JsonSuccess, xrender, redirecterror, url_valid
from community.models import ShortLink
from django.core.context_processors import csrf
from community.forms import ShortLinkForm
from django.views.decorators.http import require_http_methods

@login_required
def manage_shortlink(request):
    params = {}
    params['form'] = ShortLinkForm()
    params.update(csrf(request))
    return xrender(request, 'manage_shortlink.html', params)

@require_http_methods(["POST", ])
@login_required
def add_shortlink(request):
    try:
        if not request.POST.get('shortname') or not request.POST.get('url'):
            return JsonError('Must provide both shortname and url.')
        shortname = request.POST['shortname']
        user_profile = request.user.profile
        url = request.POST['url']
        if not url_valid(url):
            return JsonError('Url format incorrect (common mistake: must start with http or https)')
        if ShortLink.objects.filter(shortname=shortname, user_profile=user_profile).count():
            return JsonError('Name already in use.')
        ShortLink.objects.create(shortname=shortname, url=url, user_profile=user_profile)
        return JsonSuccess('Shortlink is successfully added.')
    except Exception as e:
        print repr(e)
        return JsonError('Unknown error')

@login_required
def redirect_shortlink(request, shortname):
    try:
        linkobj = ShortLink.objects.get(user_profile=request.user.profile, shortname=shortname)
        return redirect(to=linkobj.url, permanent=True)
    except ShortLink.DoesNotExist:
        return redirecterror(request, 'Shortlink not found.')
    except Exception as e:
        print repr(e)
        return redirecterror(request, 'Multiple instances found or shortlink points to invalid url.')

@login_required
def edit_shortlink(request, shortname):
    link_obj_list = ShortLink.objects.filter(user_profile=request.user.profile, shortname=shortname)
    if request.method == 'POST':
        if not request.POST.get('shortname') or not request.POST.get('url'):
            return JsonError('Must provide both shortname and url.')
        if not link_obj_list.count():
            return JsonError('Shortlink not found.')
        if link_obj_list.count() > 1:
            return JsonError('Multiple ShortLink instances found.')
        url = request.POST['url']
        shortname = request.POST['shortname']
        linkobj = link_obj_list[0]
        print url
        if not url_valid(url):
            return JsonError('Url format incorrect (common mistake: must start with http or https)')
        if linkobj.shortname != shortname and ShortLink.objects.filter(shortname=shortname, user_profile=user_profile).count():
            return JsonError('Name already in use.')
        linkobj.shortname = shortname
        linkobj.url = url
        linkobj.save()
        return JsonSuccess('Updated.')
    else:
        if not link_obj_list.count():
            return redirecterror(request, 'Shortlink not found.')
        if link_obj_list.count() > 1:
            return redirecterror(request, 'Multiple ShortLink instances found.')
        linkobj = link_obj_list[0]
        params = {}
        params['form'] = ShortLinkForm(instance=linkobj)
        params['shortlink'] = linkobj
        params.update(csrf(request))
        return xrender(request, 'edit_shortlink.html', params)

@login_required
def delete_shortlink(request, shortname):
    try:
        linkobj = ShortLink.objects.get(user_profile=request.user.profile, shortname=shortname)
        linkobj.delete()
        return redirect('manage_shortlink')
    except ShortLink.DoesNotExist:
        return redirecterror(request, 'Shortlink not found.')
    except Exception as e:
        print repr(e)
        return redirect('index')
