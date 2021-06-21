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
    instance.upper_left = features[0]
    instance.upper_right = features[2]
    instance.lower_left = features[1]
    instance.lower_middle = features[3]
    instance.lower_right = features[4]
    instance.save()
    logger.info('Case features updated!')


@transaction.atomic
def lock_instance(instance) -> None:
    logger.info('Locking instance...')
    instance.lock = True
    instance.save()
    logger.info('Instance locked!')


@transaction.atomic
def unlock_instance(instance) -> None:
    logger.info('Unlocking instance...')
    instance.lock = False
    instance.save()
    logger.info('Instance unlocked!')
