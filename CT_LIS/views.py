from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import CreateAPIView

from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser

from CT_LIS.models import CTLungInfectionSegmentation
from CT_LIS.serializers import CTLungInfectionSegmentationSerializers


class CTLungInfectionSegmentationSerializersView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # parser_classes = [FileUploadParser]
    serializer_class = CTLungInfectionSegmentationSerializers
    queryset = CTLungInfectionSegmentation.objects.all()

    # lookup_url_kwarg = 'id'

    # def get_serializer_class(self):
    #     return CTLungInfectionSegmentationSerializers

    # def filter_queryset(self, queryset):
    #     queryset = self.get_queryset().filter(prescriber=self.request.user)
    #     return queryset

    # def pre_save(self, obj):
    #     obj.prescriber = self.request.user
    #     obj.file = self.request.FILES.get('file')
