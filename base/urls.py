from django.urls import path
from .views import SignUpView, AwardPoint, UpdatePoint, deletePoint, awarded


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("award-point/", AwardPoint, name="award-point"),
    path("update-point/<str:pk>/", UpdatePoint, name="update-point"),
    path("delete-point/<str:pk>/", deletePoint, name="delete-point"),
    path("teacher/", awarded, name="teacher")
]
