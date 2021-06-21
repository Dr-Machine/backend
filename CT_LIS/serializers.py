from rest_framework import serializers

from accounts.serializers import CustomUserSerializers

from CT_LIS.models import CTLungInfectionSegmentation


class CTLungInfectionSegmentationSerializers(serializers.ModelSerializer):
    prescriber = CustomUserSerializers()

    class Meta:
        model = CTLungInfectionSegmentation
        fields = [
            'id',
            'timestamp',
            'is_deleted',
            'patient_id',
            'patient_sex',
            'patient_age',
            'upper_left',
            'upper_right',
            'lower_left',
            'lower_middle',
            'lower_right',
        ]
