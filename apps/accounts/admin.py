from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['username']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('StudentHub Role & Extra Info', {'fields': ('role', 'phone', 'profile_picture', 'bio')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('StudentHub Role & Extra Info', {'fields': ('role', 'phone', 'email', 'first_name', 'last_name')}),
    )
