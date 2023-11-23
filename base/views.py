from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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
    """listing the awarded points"""
    point = PointTransaction.objects.get(id=pk)
    form = AwardForm(instance=point)
    if request.method == 'POST':
        form = AwardForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
            return redirect('teacher')

    context = {'form': form}
    return render(request, "base/award_point.html", context)


def awarded(request):
    """listing the awarded points"""
    points = PointTransaction.objects.all()
    context = {'points': points}
    return render(request, "base/teacher_dashboard.html", context)