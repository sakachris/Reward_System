'''from django.urls import path
from .views import SignUpView, AwardPoint, UpdatePoint, deletePoint, awarded, student_home


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path("award-point/", AwardPoint, name="award-point"),
    path("update-point/<str:pk>/", UpdatePoint, name="update-point"),
    path("delete-point/<str:pk>/", deletePoint, name="delete-point"),
    path("teacher/", awarded, name="teacher"),
    # path("student/", student_home, name="student")
]'''

# urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import teachers_dashboard, students_dashboard, CustomLoginView, AwardPoint, UpdatePoint, deletePoint

urlpatterns = [
    #path('', CustomLoginView.as_view(), name='custom_login'),
    path('teachers/dashboard/', teachers_dashboard, name='teachers_dashboard'),
    #path("teacher/", awarded, name="teacher"),
    path('students/dashboard/', students_dashboard, name='students_dashboard'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("award-point/", AwardPoint, name="award-point"),
    path("update-point/<str:pk>/", UpdatePoint, name="update-point"),
    path("delete-point/<str:pk>/", deletePoint, name="delete-point"),
    # Other URLs...
]
