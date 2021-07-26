from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active','user_type')
    search_fields = ('email','user_type')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)