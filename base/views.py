from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, AwardForm
from .models import PointTransaction, CustomUser
from django.shortcuts import get_object_or_404


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

def redeempoints(request, pk):
    """select an award you have enough points for"""
    award = get_object_or_404(AwardItems, id=pk)
    student = get_object_or_404(CustomUser, is_student=True, id=request.user.id)

    if student.points >= award.points:
        redeemed = RedeemAward.objects.create(
            select_award = award,
            student = student,
            date_redeemed = timezone.now())
    student.points -= award.points
    student.save()

    return JsonResponse({"message": "Redeeming Succesful"})


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

    for award in awards:
        if award.student not in unique_student_names:
            unique_students.append(award)
            unique_student_names.add(award.student)

    pts = {}
    for i in unique_students:
        stud = i.student
        # Get the total points for the student
        total_points = PointTransaction.objects.filter(student=stud).aggregate(Sum('category__point'))['category__point__sum']
        pts[i.student.username] = total_points
    
    # print(pts)
    # print(pts['student1'])
    ptss = sorted(pts.items(), key=lambda x: x[1], reverse=True)
    context = {'points': points, 'names': unique_students, 'ptss': ptss}
    return render(request, "base/teacher_dashboard.html", context)