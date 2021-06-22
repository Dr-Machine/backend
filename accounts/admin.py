from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff',
                    'is_active', 'last_login')
    list_filter = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',
                   'last_login')
    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')
        }),
    )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('email', 'first_name', 'last_name', 'password1',
                   'password2', 'is_staff', 'is_active', 'is_superuser')
    }), )
    search_fields = ('email', )
    ordering = ('email', )


# class ProfileAdmin(admin.ModelAdmin):
#     model = Profile
#     list_display = ('user', 'email_confirmed', 'mobile', 'mobile_confirmed',
#                     'national_id', 'national_id_confirmed')
#     list_filter = ('user', 'email_confirmed', 'mobile', 'mobile_confirmed',
#                    'national_id', 'national_id_confirmed')

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Profile, ProfileAdmin)
