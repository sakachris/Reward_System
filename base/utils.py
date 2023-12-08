# base/utils.py

from .models import School
from threading import local

_thread_locals = local()

def set_current_tenant(school):
    _thread_locals.current_school = school

def get_current_tenant():
    return getattr(_thread_locals, 'current_school', None)

def get_school_from_request(request):
    subdomain = request.get_host().split('.')[0]  # Get the subdomain from the request
    try:
        return School.objects.get(subdomain=subdomain)
    except School.DoesNotExist:
        # Handle the case where the school cannot be determined
        return None
