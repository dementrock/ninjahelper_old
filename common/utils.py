from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson
import uuid

ERROR_STATUS = {'status': 'Error'}

def generate_username():
    return uuid.uuid4().hex[0:30]

class JsonResponse(HttpResponse):
    def __init__(self, data):
        print data
        content = simplejson.dumps(data, indent=2, ensure_ascii=False)
        print content
        super(JsonResponse, self).__init__(content=content)
