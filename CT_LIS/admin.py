from django.contrib import admin

from CT_LIS.models import CTLungInfectionSegmentation


class CTLungInfectionSegmentationAdmin(admin.ModelAdmin):
    model = CTLungInfectionSegmentation
    list_display = ('id', 'prescriber', 'timestamp', 'patient_id',
                    'patient_sex', 'patient_age', 'is_deleted')
    list_filter = ('id', 'prescriber', 'timestamp', 'patient_id',
                   'patient_sex', 'patient_age', 'is_deleted')


admin.site.register(CTLungInfectionSegmentation,
                    CTLungInfectionSegmentationAdmin)
