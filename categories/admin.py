from django.contrib import admin

# Register your models here.
from .models import Student, Activity, StudentPoints

class StudentAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'admin_no')

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'show_students')
    def show_students(self, obj):
        return ', '.join([student.first_name + ' ' + student.last_name for student in obj.students.all()])
    show_students.short_description = 'Students'

admin.site.register(Student, StudentAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(StudentPoints)