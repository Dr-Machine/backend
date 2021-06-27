import logging

from django.db import transaction

logger = logging.getLogger('backend')


@transaction.atomic
def update_case_metadata(instance, metadata) -> None:
    logger.info('Updating case metadata...')
    instance.patient_id = metadata['PatientID']
    instance.patient_sex = metadata['PatientSex']
    instance.patient_age = int(metadata['PatientAge'][:-1])
    instance.save()
    logger.info('Case metadata updated!')


@transaction.atomic
def update_case_features(instance, features) -> None:
    logger.info('Updating case features...')
    instance.normal = features[0]
    instance.pneumonia = features[2]
    instance.covid = features[1]
    instance.save()
    logger.info('Case features updated!')
