from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .views import (
        teachers_dashboard,
        students_dashboard,
        CustomLoginView,
        award_point,
        update_point,
        delete_point,
        redeem_point,
        student_points,
        student_awards,
        points_awarded,
        points_redeemed
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
    path("student-points/", student_points, name="student-points"),
    path("student-awards/", student_awards, name="student-awards"),
    path("points-awarded/", points_awarded, name="points-awarded"),
    path("points-redeemed/", points_redeemed, name="points-redeemed"),
    path('password_change/', PasswordChangeView.as_view(template_name='base/registration/password_change_form.html', success_url=reverse_lazy('password_change_done')), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='base/registration/password_change_done.html'), name='password_change_done'),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name='base/registration/password_reset_form.html'), name="reset_password"),
    #path('password_reset/', PasswordResetView.as_view(template_name='base/registration/password_reset_form.html', email_template_name='registration/password_reset_email.html', success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='base/registration/password_reset_done.html'), name='password_reset_done'),
    #path('password_reset/done/', PasswordResetDoneView.as_view(template_name='base/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='base/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    #path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='base/registration/password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='base/registration/password_reset_complete.html'), name='password_reset_complete'),
    #path('reset/done/', PasswordResetCompleteView.as_view(template_name='base/registration/password_reset_complete.html'), name='password_reset_complete'),
]
