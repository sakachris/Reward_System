from django.urls import path
from .views import SignUpView, AwardPoint, UpdatePoint, awarded


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("award-point/", AwardPoint, name="award-point"),
    path("update-point/<str:pk>/", UpdatePoint, name="update-point"),
    path("teacher/", awarded, name="teacher")
]
