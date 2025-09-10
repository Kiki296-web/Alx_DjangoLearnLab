from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('bio', 'profile_picture', 'followers')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra', {'fields': ('bio', 'profile_picture')}),
    )

admin.site.register(User, CustomUserAdmin)
