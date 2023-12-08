from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
        PointCategory,
        CustomUser,
        StudentProfile,
        TeacherProfile,
        AwardItem,
        School
)


class CustomUserAdmin(UserAdmin):
    """ customizing admin field """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (
            'User Details',
            {'fields': ('username', 'email', 'first_name', 'last_name')}
        ),
        (
            'User Type',
            {'fields': ('is_student', 'is_teacher')}
        ),
    )
    list_display = [
            "username", "first_name", "last_name", "is_student", "is_teacher"
    ]


class PointCategoryAdmin(admin.ModelAdmin):
    """ customizing point category fields """
    list_display = ["name", "created_at", "updated_at", "point", "description"]


class AwardItemAdmin(admin.ModelAdmin):
    """ customizing award item fields """
    list_display = ["name", "points", "description", "units", "created_at"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PointCategory, PointCategoryAdmin)
admin.site.register(AwardItem, AwardItemAdmin)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """ customizing Student Profile fields view """
    list_display = ('user', 'grade', 'adm_no', 'parent_contact')

    def user(self, obj):
        return obj.user.username


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    """ customizing Teacher Profile fields view """
    list_display = ('user', 'designation', 'reg_no', 'contact')

    def user(self, obj):
        return obj.user.username


class SchoolAdmin(UserAdmin):
    list_display = ('name', 'subdomain', 'admin_user', 'school')  # Update based on your needs
    search_fields = ('name', 'subdomain')
    readonly_fields = ('admin_user',)

    fieldsets = (
        (None, {'fields': ('name', 'subdomain')}),
        ('Admin User', {'fields': ('admin_user',)}),
        ('School', {'fields': ('school',)}),  # Add this line to include the school in the admin
    )

admin.site.register(School, SchoolAdmin)