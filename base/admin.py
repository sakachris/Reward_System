from django.contrib import admin
from .models import PointCategory, PointTransaction
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
        PointCategory,
        CustomUser,
        StudentProfile,
        TeacherProfile,
        AwardItem
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
# admin.site.register(PointTransaction)
admin.site.register(AwardItem, AwardItemAdmin)
# admin.site.register(RedeemAward)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade', 'adm_no', 'parent_contact')

    # Customize the display of the user field
    def user(self, obj):
        return obj.user.username


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'reg_no', 'contact')

    # Customize the display of the user field
    def user(self, obj):
        return obj.user.username
