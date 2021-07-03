import logging

from time import sleep

from backend.celery import app

from ai_corona.core.model import COVID19DiagnosisModel
from ai_corona.models import COVID19Diagnosis
from ai_corona.transactions import update_case_features

logger = logging.getLogger('backend')


@app.task(name='ai_corona.execute_run_mode')
def execute_run_model(case_directory_path: str, id: str) -> None:
    logger.info('Executing run model...')

    instance = COVID19Diagnosis.objects.get(id=id)

    model = COVID19DiagnosisModel()

    logger.info('Model is extracting features...')
    features = model.run(case_directory_path=case_directory_path)
    # sleep(10)
    # features = [0.1, 0.2, 0.3]
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
