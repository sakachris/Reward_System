from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, AwardForm, CustomAuthenticationForm
from .models import PointTransaction, CustomUser
from django.http import HttpResponse


'''class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "base/signup.html"'''

'''class CustomLoginView(LoginView):
    def get_success_url(self):
        # Redirect based on user role
        if self.request.user.is_student:
            return '/student/'  # Update with your actual URL
        elif self.request.user.is_teacher:
            return '/teacher/'  # Update with your actual URL
        else:
            # Redirect to a default page if neither is_student nor is_teacher is True
            return ''  # Update with your actual URL'''

'''def student_home(request):
    return render(request, 'student_home.html')'''

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

#@login_required(login_url='login')
@user_passes_test(lambda u: u.is_authenticated and u.is_teacher, login_url='login')
def teachers_dashboard(request):
    """listing the awarded points"""
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    points = PointTransaction.objects.filter(
        Q(description__icontains=q) |
        Q(date__icontains=q) |
        Q(student__username__icontains=q) |
        Q(category__name__icontains=q)
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
    return render(request, "base/teachers_dashboard.html", context)

def students_dashboard(request):
    """listing the awarded points"""
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    points = PointTransaction.objects.filter(
        Q(student=request.user) &
        (Q(description__icontains=q) |
        Q(date__icontains=q) |
        Q(student__username__icontains=q) |
        Q(category__name__icontains=q))
    )
    # points = PointTransaction.objects.all()
    '''awards = PointTransaction.objects.all()
    unique_student_names = set()
    unique_students = []

    for award in awards:
        if award.student not in unique_student_names:
            unique_students.append(award)
            unique_student_names.add(award.student)

    pts = {}
    for i in unique_students:
        stud = i.student'''
        # Get the total points for the student
    total_points = PointTransaction.objects.filter(student=request.user).aggregate(Sum('category__point'))['category__point__sum']
        #pts[i.student.username] = total_points
    
    # print(pts)
    # print(pts['student1'])
    #ptss = sorted(pts.items(), key=lambda x: x[1], reverse=True)
    context = {'points': points, 'total': total_points}
    return render(request, "base/students_dashboard.html", context)


# views.py
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        #user_type = self.request.user.user_type
        if self.request.user.is_teacher:
        #if user_type == 'is_teacher':
            return reverse_lazy('teachers_dashboard')
        elif self.request.user.is_student:
        #elif user_type == 'is_student':
            return reverse_lazy('students_dashboard')
        else:
            # Default to some other URL if user_type is not specified
            return reverse_lazy('admin:index')  # Adjust 'home' to your default URL
            #return HttpResponse("Hello, world. You're at the polls index.")
