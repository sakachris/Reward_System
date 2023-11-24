from django.db import models
#from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	admin_no = models.IntegerField()

	def __str__(self):
		return f"{self.first_name} {self.last_name}"


class Activity(models.Model):
	students = models.ManyToManyField(Student)
	title = models.CharField(max_length=150)
	points = models.IntegerField()
	description = models.TextField(null=True, blank=False)
#	created_at = models.DateTimeField(auto_now_add=True)
#	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		std_names = ', '.join([f"{student.first_name} {student.last_name}" for student in self.students.all()])
		return f"{self.title} {self.points} {std_names}"

class StudentPoints(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
#	activities = Activity.objects.filter(students__first_name='Mercy') [act.points for act in activities]

#pts = student, categories, desc. Categories is activities