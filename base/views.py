from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, AwardForm
from .models import PointTransaction


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "base/signup.html"


def AwardPoint(request):
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


def awarded(request):
    """listing the awarded points"""
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    points = PointTransaction.objects.filter(
        Q(description__icontains=q) |
        Q(date__icontains=q) |
        Q(student__username__icontains=q)
    )
    # points = PointTransaction.objects.all()
    awards = PointTransaction.objects.all()
    unique_student_names = set()
    unique_students = []
    # awarded_points = {}

    for award in awards:
        # awarded_points[award.student] = award.category.point
        if award.student not in unique_student_names:
            unique_students.append(award)
            unique_student_names.add(award.student)
    # print(awarded_points)
    context = {'points': points, 'names': unique_students}
    return render(request, "base/teacher_dashboard.html", context)