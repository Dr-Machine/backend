import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from ai_corona.models import COVID19Diagnosis
from ai_corona.tasks import execute_run_model
from ai_corona.transactions import update_case_metadata

from utils.dicom_utils import read_metadata
from utils.misc import (extract_zipfile_case,
                        validate_result_directory_existence, find_a_dicom_file)

logger = logging.getLogger('backend')


@receiver(post_save, sender=COVID19Diagnosis)
def run_COVID19Diagnosis(sender, instance, created, **kwargs):
    if created:
        logger.info('Running functions at creating new CT lung '
                    'infection segmentation case ...')

        extract_zipfile_case(instance.file.path, instance.case_directory_path)

        _file = find_a_dicom_file(
            case_directory_path=instance.case_directory_path)
        metadata = read_metadata(_file)
        update_case_metadata(instance=instance, metadata=metadata)

        # validate_result_directory_existence(
        #     result_directory_path=instance.result_directory_path)

        logger.info('Functions at creating new CT lung '
                    'infection segmentation case done!')
