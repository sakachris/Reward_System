from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.views.generic.edit import CreateView
from .forms import (
        CustomUserCreationForm,
        AwardForm,
        CustomAuthenticationForm,
        ReedemForm
)
from .models import PointTransaction, CustomUser, StudentProfile, RedeemAward
from django.http import HttpResponse


@user_passes_test(lambda u: u.is_authenticated and u.is_teacher,
                  login_url='login')
def award_point(request):
    """ view for awarding points to students """
    form = AwardForm()

    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            current_user = request.user

            # Check if the user is a teacher
            if current_user.is_authenticated and current_user.is_teacher:
                # Set the teacher ID before saving the form
                form.instance.teacher_id = current_user.id
                form.save()
                messages.success(request, "Point Awarded Successfully")
                return redirect('award-point')
                # return redirect('teachers_dashboard')
            else:
                # Handle the case where the user is not a teacher
                pass
                # msg = {'error_msg': 'not authorized to perform this action'}
                # return render(request, 'error_page.html', msg)

    context = {'form': form}
    return render(request, "base/award_point.html", context)


@user_passes_test(lambda u: u.is_authenticated and u.is_teacher,
                  login_url='login')
def update_point(request, pk):
    """Updates awarded point"""
    point = PointTransaction.objects.get(id=pk)
    form = AwardForm(instance=point)
    if request.method == 'POST':
        form = AwardForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
            messages.success(request, "Point Edited Successfully")
            return redirect('award-point')
            # return redirect('teachers_dashboard')

    context = {'form': form}
    return render(request, "base/award_point.html", context)


@user_passes_test(lambda u: u.is_authenticated and u.is_teacher,
                  login_url='login')
def delete_point(request, pk):
    """deletes a point awarded"""
    point = PointTransaction.objects.get(id=pk)
    if request.method == 'POST':
        point.delete()
        return redirect('teachers_dashboard')

    return render(request, "base/delete.html", {'obj': point})


@user_passes_test(lambda u: u.is_authenticated and u.is_teacher,
                  login_url='login')
def teachers_dashboard(request):
    """listing the awarded points"""
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    points = PointTransaction.objects.filter(
        Q(teacher=request.user) &
        (
            Q(description__icontains=q) |
            Q(created_at__icontains=q) |
            Q(student__username__icontains=q) |
            Q(category__name__icontains=q)
        )
    )
    items = RedeemAward.objects.filter(
        Q(select_award__name__icontains=q) |
        Q(date_redeemed__icontains=q) |
        Q(student__username__icontains=q) |
        Q(select_award__points__icontains=q)
    )

    awards = PointTransaction.objects.values('student__username').distinct()
    pts = {
        award['student__username']: (
            PointTransaction.objects
            .filter(student__username=award['student__username'])
            .aggregate(Sum('category__point'))['category__point__sum'] or 0
        )
        for award in awards
    }
    ptss = sorted(pts.items(), key=lambda x: x[1], reverse=True)

    redeems = RedeemAward.objects.values('student__username').distinct()
    rdm = {
        redeem['student__username']: (
            RedeemAward.objects
            .filter(student__username=redeem['student__username'])
            .aggregate(Sum('select_award__points'))
            .get('select_award__points__sum', 0) or 0
        )
        for redeem in redeems
    }
    rdms = sorted(rdm.items(), key=lambda x: x[1], reverse=True)

    context = {
            'points': points,
            'rdms': rdms,
            'ptss': ptss,
            'items': items
    }
    return render(request, "base/teachers_dashboard.html", context)


@user_passes_test(lambda u: u.is_authenticated and u.is_student,
                  login_url='login')
def students_dashboard(request):
    """listing the awarded points"""
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    '''points = PointTransaction.objects.filter(
        Q(student=request.user) &
        (
            Q(description__icontains=q) |
            Q(created_at__icontains=q) |
            Q(student__username__icontains=q) |
            Q(category__name__icontains=q)
        )
    )'''
    points = PointTransaction.objects.filter(student=request.user).order_by('-created_at')[:4]
    # Get the total points for the student
    total_points = (
            PointTransaction.objects.filter(student=request.user)
            .aggregate(Sum('category__point'))['category__point__sum'] or 0
    )
    total_redeemed = (
            RedeemAward.objects.filter(student=request.user)
            .aggregate(Sum('select_award__points'))
            .get('select_award__points__sum', 0) or 0
    )
    points_balance = total_points - total_redeemed

    bios = StudentProfile.objects.filter(user=request.user)[0]

    redeemed_items = RedeemAward.objects.filter(student=request.user).order_by('-date_redeemed')[:4]

    context = {
            'points': points,
            'total': total_points,
            'bios': bios,
            'items': redeemed_items,
            'redeemed': total_redeemed,
            'balance': points_balance
    }

    return render(request, "base/students_dashboard.html", context)


class CustomLoginView(LoginView):
    """ class for logging in users """
    form_class = CustomAuthenticationForm
    template_name = 'base/login.html'

    def get_success_url(self):
        if self.request.user.is_teacher:
            return reverse_lazy('teachers_dashboard')
        elif self.request.user.is_student:
            return reverse_lazy('students_dashboard')
        else:
            return reverse_lazy('admin:index')


@user_passes_test(lambda u: u.is_authenticated and u.is_student,
                  login_url='login')
def redeem_point(request):
    """ view for awarding points to students """
    # form = ReedemForm()

    if request.method == 'POST':
        form = ReedemForm(request.POST, request=request)
        if form.is_valid():
            current_user = request.user
            # Check if the user is a student
            if current_user.is_authenticated and current_user.is_student:
                # Set the student ID before saving the form
                form.instance.student_id = current_user.id
            form.save()
            messages.success(request, "Award Redeemed Successfully")
            return redirect('redeem-point')
    else:
        form = ReedemForm(request=request)

    return render(request, 'base/redeem_point.html', {'form': form})
