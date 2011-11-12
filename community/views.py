from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from community.utils import fetch_course_data, fetch_friend_data, fetch_compare_data
from common.utils import JsonResponse, ERROR_STATUS
from django.contrib.auth.models import User
import hashlib


def import_course_data(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return JsonResponse(ERROR_STATUS)
    try:
        return JsonResponse(fetch_course_data(username=username, password=password))
    except Exception as e:
        print e
        return JsonResponse(ERROR_STATUS)

def import_friend_data(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return JsonResponse(ERROR_STATUS)
    try:
        return JsonResponse(fetch_friend_data(username=username, password=password))
    except Exception as e:
        print e
        return JsonResponse(ERROR_STATUS) 

def compare_schedule(request):
    print request.POST
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return JsonResponse(ERROR_STATUS)
    try:
        return JsonResponse(fetch_compare_data(username=username, password=password))
    except Exception as e:
        print e
        return JsonResponse(ERROR_STATUS)
