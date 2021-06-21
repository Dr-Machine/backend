import logging

import os
from os import listdir
from os.path import isfile, join

import zipfile

logger = logging.getLogger('backend')


def extract_zipfile_case(zipfile_path: str, extract_path: str) -> None:
    logger.info('Proceding to extract zipfile case...')
    try:
        with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        os.remove(zipfile_path)
        logger.info('Zipfile case extracted!')
    except Exception as e:
        message = (f'Failed to extract zipfile case. Reason: {str(e)}.')
        logger.error(message)


def validate_result_directory_existence(result_directory_path: str) -> None:
    logger.info('Proceding to create results directory...')
    try:
        if not os.path.isdir(result_directory_path):
            os.makedirs(result_directory_path)
        logger.info('Results directory created!')
    except Exception as e:
        message = (f'Failed to create results directory. Reason: {str(e)}.')
        logger.error(message)


def find_a_dicom_file(case_directory_path: str) -> str:
    logger.info('Proceding to find a DICOM file...')
    try:
        files = [
            f for f in listdir(case_directory_path)
            if isfile(join(case_directory_path, f))
        ]
        file = f'{case_directory_path}/{files[0]}'
        logger.info('Found a DICOM file!')
        return file
    except Exception as e:
        message = (f'Failed to find a DICOM file. Reason: {str(e)}.')
        logger.error(message)
