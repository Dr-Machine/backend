import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from ai_corona.models import COVID19Diagnosis
from ai_corona.transactions import update_case_metadata

from utils.dicom_utils import read_metadata
from utils.misc import extract_zipfile_case, find_a_dicom_file

logger = logging.getLogger('backend')


@receiver(post_save, sender=COVID19Diagnosis)
def COVID19DiagnosisSignal(sender, instance, created, **kwargs):
    if created:
        logger.info('Running functions at new COVID-19 '
                    'diagnosis case creation...')

        extract_zipfile_case(instance.file.path, instance.case_directory_path)

        _file = find_a_dicom_file(
            case_directory_path=instance.case_directory_path)
        metadata = read_metadata(_file)
        update_case_metadata(instance=instance, metadata=metadata)

        logger.info('Functions at new COVID-19 '
                    'diagnosis case creation done!')
