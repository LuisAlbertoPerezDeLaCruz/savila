# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
    list_display = ["email", "username", "is_instructor"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_instructor',)}),
    )


admin.site.register(User, UserAdmin)
