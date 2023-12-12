from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django.apps import apps
from .models import School, Domain
from django_tenants.utils import get_public_schema_name


@admin.register(School)
class RestrictedModelAdmin(admin.ModelAdmin):

    list_display = ('name', 'created_on')

    def has_view_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False

    def has_change_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False

    def has_add_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False

    def has_delete_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False


@admin.register(Domain)
class RestrictedsModelAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        # Get the model associated with this admin instance
        model = self.model
        field_names = [field.name for field in model._meta.get_fields()]
        return field_names

    def has_change_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False

    def has_add_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False

    def has_delete_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False

    def has_view_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False


'''app = apps.get_app_config('schools')
for model_name, model in app.models.items():
    # Get all field names of the model
    field_names = [field.name for field in model._meta.get_fields()]
    #admin.site.register(model, RestrictedModelAdmin)'''
