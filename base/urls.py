from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
        teachers_dashboard,
        students_dashboard,
        CustomLoginView,
        award_point,
        update_point,
        delete_point,
        redeem_point
)

urlpatterns = [
    path('teachers/dashboard/', teachers_dashboard, name='teachers_dashboard'),
    path('students/dashboard/', students_dashboard, name='students_dashboard'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("award-point/", award_point, name="award-point"),
    path("redeem-point/", redeem_point, name="redeem-point"),
    path("update-point/<str:pk>/", update_point, name="update-point"),
    path("delete-point/<str:pk>/", delete_point, name="delete-point"),
]
