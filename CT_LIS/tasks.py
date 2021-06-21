import logging

from backend.celery import app

from CT_LIS.core.model import CTLungInfectionSegmentationModel
from CT_LIS.models import CTLungInfectionSegmentation
from CT_LIS.transactions import (update_case_features, lock_instance,
                                 unlock_instance)

logger = logging.getLogger('backend')


@app.task(name='CT_LIS.execute_run_mode')
def execute_run_model(case_directory_path: str, result_directory_path: str,
                      id) -> None:
    print(type(id))
    logger.info('Executing run model...')

    instance = CTLungInfectionSegmentation.objects.get(id=id)

    lock_instance(instance=instance)

    model = CTLungInfectionSegmentationModel()

    logger.info('Model extracting features...')
    features = model.run(case_directory_path=case_directory_path,
                         result_directory_path=result_directory_path)
    logger.info('Model feature extraction completed!')
    logger.info(f'Extracted features are {features}.')

    logger.info('Proceding to save the extraced features...')
    try:
        update_case_features(instance=instance, features=features)
        logger.info('Extraced features saved!')
    except Exception as e:
        message = (f'Failed to save extracted features. Reason: {str(e)}.')
        logger.error(message)

    unlock_instance(instance=instance)

    logger.info('Executing run model finished!')
