from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'email_confirmed', 'mobile', 'mobile_confirmed',
                    'national_id', 'national_id_confirmed')
    list_filter = ('user', 'email_confirmed', 'mobile', 'mobile_confirmed',
                   'national_id', 'national_id_confirmed')


admin.site.register(Profile, ProfileAdmin)
