from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Role, User


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    filter_horizontal = ['permissions']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'employee_id', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'preferred_language']
    search_fields = ['email', 'first_name', 'last_name', 'employee_id']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'employee_id', 'phone', 'preferred_language'),
        }),
        ('Role et permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
        }),
        ('Securite', {
            'fields': ('must_change_password', 'last_login_ip', 'last_login'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'employee_id', 'first_name', 'last_name',
                'role', 'password1', 'password2',
            ),
        }),
    )
