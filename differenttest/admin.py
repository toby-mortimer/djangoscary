from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserAdminConfig(UserAdmin):
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'is_active')


admin.site.register(NewUser, UserAdminConfig)

