from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Security Question", {"fields": ("security_question_answer",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)