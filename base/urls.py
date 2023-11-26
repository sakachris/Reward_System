from django.urls import path
from .views import SignUpView, AwardPoint, UpdatePoint, deletePoint, awarded, student_home


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path("award-point/", AwardPoint, name="award-point"),
    path("update-point/<str:pk>/", UpdatePoint, name="update-point"),
    path("delete-point/<str:pk>/", deletePoint, name="delete-point"),
    path("teacher/", awarded, name="teacher"),
    # path("student/", student_home, name="student")
]
