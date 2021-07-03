import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ai_corona.models import COVID19Diagnosis
from ai_corona.serializers import COVID19DiagnosisSerializers
from ai_corona.tasks import execute_run_model

logger = logging.getLogger('backend')


class COVID19DiagnosisView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = COVID19Diagnosis.objects.all()
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        return COVID19DiagnosisSerializers

    def filter_queryset(self, queryset):
        queryset = self.get_queryset().filter(prescriber=self.request.user)
        return queryset

    @action(detail=True, methods=['GET'])
    def run(self, request, *args, **kwargs):
        case_object = self.get_object()

        try:
            logger.info('Proceding to add the COVID-19 '
                        'diagnosis task to the task queue...')

            execute_run_model.delay(
                case_directory_path=case_object.case_directory_path,
                id=case_object.id)

            message = ('COVID-19 diagnosis task was '
                       'successfully added to the task queue!')
            logger.info(message)
            data = {'detail': message}
            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as e:
            message = ('Failed to run COVID-19 diagnosis model. '
                       f'Reason: {str(e)}.')
            logger.error(message)
            data = {'detail': message}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
