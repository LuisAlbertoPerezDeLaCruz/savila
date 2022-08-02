# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
    list_display = ["email", "username","is_plugged", "is_instructor", "is_bot"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_plugged','is_instructor', 'is_bot')}),
    )


admin.site.register(User, UserAdmin)
