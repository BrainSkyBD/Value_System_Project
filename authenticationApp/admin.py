from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view of users
    list_display = ('username', 'email', 'phone_number', 'User_Role', 'is_staff', 'is_active')
    # Fields that can be searched in the admin
    search_fields = ('username', 'email', 'phone_number', 'User_Role')
    # Filters on the right-hand side
    list_filter = ('User_Role', 'is_staff', 'is_active', 'is_superuser')
    # Group fields into sections in the detail form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'phone_number')}),
        ('Permissions', {'fields': ('User_Role', 'is_staff', 'is_active', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Fields that appear when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'User_Role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    # Read-only fields in the admin
    readonly_fields = ('date_joined', 'last_login')

admin.site.register(User, CustomUserAdmin)
