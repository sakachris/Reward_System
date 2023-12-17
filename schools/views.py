from django.shortcuts import render, redirect, get_object_or_404
from .models import School
from django.db.models import Q


def search_and_redirect(request):
    """listing the awarded points"""
    q = request.GET.get('q')
    if q is not None and q != "":
        points = School.objects.filter(Q(schema_name__icontains=q))
    else:
        points = {}
    return render(request, 'schools/search.html', {'schools': points})


def school_login(request, schema_name):
    school = School.objects.get(schema_name=schema_name)
    domain = school.domains.all()[0]

    return redirect(f'http://{domain}:8000')
    # return redirect(f'http://{domain}')
