from django.contrib import admin

from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'email_confirmed', 'mobile', 'mobile_confirmed',
                    'national_id', 'national_id_confirmed')
    list_filter = ('user', 'email_confirmed', 'mobile', 'mobile_confirmed',
                   'national_id', 'national_id_confirmed')
    search_fields = ('user', )
    ordering = ('user', )


admin.site.register(Profile, ProfileAdmin)
