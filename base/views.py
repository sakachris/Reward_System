from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, AwardForm, CustomAuthenticationForm
from .models import PointTransaction, CustomUser
from django.http import HttpResponse


def AwardPoint(request):
    """ view for awarding points to students """
    form = AwardForm()
    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher')

    context = {'form': form}
    return render(request, "base/award_point.html", context)


def UpdatePoint(request, pk):
    """Updates awarded point"""
    point = PointTransaction.objects.get(id=pk)
    form = AwardForm(instance=point)
    if request.method == 'POST':
        form = AwardForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
            return redirect('teacher')

    context = {'form': form}
    return render(request, "base/award_point.html", context)


def deletePoint(request, pk):
    """deletes a point awarded"""
    point = PointTransaction.objects.get(id=pk)
    if request.method == 'POST':
        point.delete()
        return redirect('teacher')

    return render(request, "base/delete.html", {'obj': point})


@user_passes_test(lambda u: u.is_authenticated and u.is_teacher,
                  login_url='login')
def teachers_dashboard(request):
    """listing the awarded points"""
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    points = PointTransaction.objects.filter(
        Q(description__icontains=q) |
        Q(date__icontains=q) |
        Q(student__username__icontains=q) |
        Q(category__name__icontains=q)
    )
    awards = PointTransaction.objects.all()
    unique_student_names = set()
    unique_students = []

    for award in awards:
        if award.student not in unique_student_names:
            unique_students.append(award)
            unique_student_names.add(award.student)

    pts = {}
    for i in unique_students:
        stud = i.student
        # Get the total points for the student
        total_points = (
                PointTransaction.objects.filter(student=stud)
                .aggregate(Sum('category__point'))['category__point__sum']
        )
        pts[i.student.username] = total_points

    ptss = sorted(pts.items(), key=lambda x: x[1], reverse=True)
    context = {'points': points, 'names': unique_students, 'ptss': ptss}
    return render(request, "base/teachers_dashboard.html", context)


def students_dashboard(request):
    """listing the awarded points"""
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    points = PointTransaction.objects.filter(
        Q(student=request.user) &
        (
            Q(description__icontains=q) |
            Q(date__icontains=q) |
            Q(student__username__icontains=q) |
            Q(category__name__icontains=q)
        )
    )
    # Get the total points for the student
    total_points = (
            PointTransaction.objects.filter(student=request.user)
            .aggregate(Sum('category__point'))['category__point__sum']
    )
    context = {'points': points, 'total': total_points}
    return render(request, "base/students_dashboard.html", context)


class CustomLoginView(LoginView):
    """ class for logging in users """
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        if self.request.user.is_teacher:
            return reverse_lazy('teachers_dashboard')
        elif self.request.user.is_student:
            return reverse_lazy('students_dashboard')
        else:
            return reverse_lazy('admin:index')
