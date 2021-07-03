import logging

from time import sleep

from backend.celery import app

from CT_LIS.core.model import CTLungInfectionSegmentationModel
from CT_LIS.models import CTLungInfectionSegmentation
from CT_LIS.transactions import update_case_features

logger = logging.getLogger('backend')


@app.task(name='CT_LIS.execute_run_mode')
def execute_run_model(case_directory_path: str, result_directory_path: str,
                      id: str) -> None:
    logger.info('Executing run model...')

    instance = CTLungInfectionSegmentation.objects.get(id=id)

    # model = CTLungInfectionSegmentationModel()

    logger.info('Model is extracting features...')
    # features = model.run(case_directory_path=case_directory_path,
    #                      result_directory_path=result_directory_path)
    sleep(10)
    features = [0.1, 0.2, 0.3, 0.4, 0.5]
    logger.info('Model feature extraction completed!')
    logger.info(f'Extracted features are {features}.')

    logger.info('Proceding to save the extraced features...')
    try:
        update_case_features(instance=instance, features=features)
        logger.info('Extraced features saved!')
    except Exception as e:
        message = (f'Failed to save extracted features. Reason: {str(e)}.')
        logger.error(message)

    logger.info('Executing run model finished!')


# stress --cpu 35 --vm 50 --vm-bytes 2048M --timeout 300s
