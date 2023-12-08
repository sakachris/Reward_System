# base/middleware.py

from django.utils.deprecation import MiddlewareMixin
from .models import School
from .utils import set_current_tenant

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_school = get_school_from_request(request)
        set_current_tenant(current_school)

    def process_response(self, request, response):
        set_current_tenant(None)  # Reset the current tenant after the request is processed
        return response
