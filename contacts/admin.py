from django.contrib import admin

from contacts.models import Contact


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    readonly_fields = ('id', )
    list_display = ('email', 'first_name', 'last_name', 'subject', 'message')
    list_filter = ('email', 'first_name', 'last_name', 'subject', 'message')
    search_fields = ('email', )
    ordering = ('email', )


admin.site.register(Contact, ContactAdmin)
