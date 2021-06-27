from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from CT_LIS.models import COVID19Diagnosis
from CT_LIS.serializers import COVID19DiagnosisSerializers


class COVID19DiagnosisView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # parser_classes = [FileUploadParser]
    serializer_class = COVID19DiagnosisSerializers
    queryset = COVID19Diagnosis.objects.all()

    # lookup_url_kwarg = 'id'

    # def get_serializer_class(self):
    #     return COVID19DiagnosisSerializers

    # def filter_queryset(self, queryset):
    #     queryset = self.get_queryset().filter(prescriber=self.request.user)
    #     return queryset

    # def pre_save(self, obj):
    #     obj.prescriber = self.request.user
    #     obj.file = self.request.FILES.get('file')
