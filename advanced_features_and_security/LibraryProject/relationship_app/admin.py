# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    """Custom admin interface for the CustomUser model."""
    
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    
    # Fields to display in the user list
    list_display = [
        'email', 
        'username', 
        'first_name', 
        'last_name', 
        'date_of_birth',
        'is_staff', 
        'is_active'
    ]
    
    # Filters in the admin
    list_filter = [
        'is_staff', 
        'is_active', 
        'date_joined', 
        'date_of_birth'
    ]
    
    # Fieldsets for viewing/editing users
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 
                'last_name', 
                'date_of_birth',
                'profile_photo'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': (
                'last_login', 
                'date_joined'
            )
        }),
    )
    
    # Fieldsets for creating new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'username', 
                'password1', 
                'password2',
                'first_name', 
                'last_name',
                'date_of_birth',
                'profile_photo'
            ),
        }),
    )
    
    # Search fields
    search_fields = ('email', 'username', 'first_name', 'last_name')
    
    # Ordering
    ordering = ('email',)
    
    # Inline editing
    filter_horizontal = ('groups', 'user_permissions',)
    
    # Readonly fields
    readonly_fields = ('last_login', 'date_joined')


# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)