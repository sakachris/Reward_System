from django.contrib import admin
from .models import PointCategory, PointTransaction
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        ('User Details', {'fields': ('username', 'email')}),
        ('User Type', {'fields': ('is_student', 'is_teacher')}),
    )
    list_display = ["username", "email", "is_student", "is_teacher"]


class PointCategoryAdmin(admin.ModelAdmin):
    # ...
    list_display = ["name", "date", "point", "description"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PointCategory, PointCategoryAdmin)
admin.site.register(PointTransaction)
