from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
        teachers_dashboard,
        students_dashboard,
        CustomLoginView,
        AwardPoint,
        UpdatePoint,
        deletePoint,
        redeempoints,
)

urlpatterns = [
    path('teachers/dashboard/', teachers_dashboard, name='teachers_dashboard'),
    path('students/dashboard/', students_dashboard, name='students_dashboard'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("award-point/", AwardPoint, name="award-point"),
    path("update-point/<str:pk>/", UpdatePoint, name="update-point"),
    path("delete-point/<str:pk>/", deletePoint, name="delete-point"),
    path("redeem-points/", redeempoints, name="redeem-point"),
]
