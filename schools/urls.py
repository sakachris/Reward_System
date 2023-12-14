from django.contrib import admin
from django.urls import path, include
from .views import search_and_redirect, school_login


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', search_and_redirect, name='search_and_redirect'),
    path('tenant/<str:schema_name>/', school_login, name='school_login')
]
