import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from CT_LIS.models import CTLungInfectionSegmentation
from CT_LIS.serializers import CTLungInfectionSegmentationSerializers
from CT_LIS.tasks import execute_run_model

logger = logging.getLogger('backend')


class CTLungInfectionSegmentationView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CTLungInfectionSegmentation.objects.all()
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        return CTLungInfectionSegmentationSerializers

    def filter_queryset(self, queryset):
        queryset = self.get_queryset().filter(prescriber=self.request.user)
        return queryset

    @action(detail=True, methods=['GET'])
    def run(self, request, *args, **kwargs):
        case_object = self.get_object()

        try:
            logger.info('Proceding to add the CT lung infection '
                        'segmentation task to the task queue...')

            execute_run_model.delay(
                case_directory_path=case_object.case_directory_path,
                result_directory_path=case_object.result_directory_path,
                id=case_object.id)

            message = ('CT lung infection segmentation task was '
                       'successfully added to the task queue!')
            logger.info(message)
            data = {'detail': message}
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
            message = ('Failed to run CT Lung Infection Segmentation model. '
                       f'Reason: {str(e)}.')
            logger.error(message)
            data = {'detail': message}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
