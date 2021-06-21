from rest_framework import viewsets

from CT_LIS.models import CTLungInfectionSegmentation
from CT_LIS.serializers import CTLungInfectionSegmentationSerializers


class CTLungInfectionSegmentationSerializersView(viewsets.ModelViewSet):
    lookup_url_kwarg = 'id'
    queryset = CTLungInfectionSegmentation.objects.all()

    def get_serializer_class(self):
        return CTLungInfectionSegmentationSerializers

    def filter_queryset(self, queryset):
        queryset = self.get_queryset().filter(creator=self.request.user)
        return queryset
