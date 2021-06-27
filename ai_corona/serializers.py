from rest_framework import serializers

from accounts.serializers import CustomUserSerializers

from ai_corona.models import COVID19Diagnosis


class COVID19DiagnosisSerializers(serializers.ModelSerializer):
    # prescriber = CustomUserSerializers()

    class Meta:
        model = COVID19Diagnosis
        fields = [
            'id',
            'prescriber',
            'timestamp',
            'is_deleted',
            'patient_id',
            'patient_sex',
            'patient_age',
            'file',
            'normal',
            'pneumonia',
            'covid',
        ]
