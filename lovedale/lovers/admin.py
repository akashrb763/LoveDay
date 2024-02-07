from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the admin interface
    list_display = ('username', 'name', 'email', 'phone_number', 'is_staff', 'is_active')
    # Define the fields that can be used to search for users
    search_fields = ('username', 'name', 'email', 'phone_number')
    # Define the fieldsets to use in the admin interface
    fieldsets = (
        (None, {'fields': ('username', 'name', 'email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'registered_date')}),
        ('Additional Information', {'fields': ('age', 'status', 'verified', 'terms_and_conditions',
                                               'profile_picture', 'cover_picture', 'bio', 'work', 'education', 'place')})
    )
    # Define the fields that can be used for adding users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

# Register your CustomUser model with the admin site using the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
