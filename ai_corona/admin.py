from django.contrib import admin

from ai_corona.models import COVID19Diagnosis


class COVID19DiagnosisAdmin(admin.ModelAdmin):
    model = COVID19Diagnosis
    list_display = [
        'id', 'prescriber', 'timestamp', 'patient_id', 'patient_sex',
        'patient_age', 'is_deleted'
    ]
    list_filter = [
        'id', 'prescriber', 'timestamp', 'patient_id', 'patient_sex',
        'patient_age', 'is_deleted'
    ]
    search_fields = ['prescriber']
    ordering = ['prescriber']


admin.site.register(COVID19Diagnosis, COVID19DiagnosisAdmin)
