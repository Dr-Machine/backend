import logging

import pydicom as dcm

logger = logging.getLogger('backend')

DATA_ELEMENTS = ['PatientID', 'PatientSex', 'PatientAge']


def read_metadata(file_path: str) -> dict:
    logger.info('Reading DICOM metadata...')
    try:
        scan = dcm.dcmread(file_path)
        metadata = {}
        for D in DATA_ELEMENTS:
            metadata[D] = scan.data_element(D).value
        logger.info('Finished reading DICOM metadata!')
        return metadata
    except Exception as e:
        message = (f'Failed to read DICOM metadata. Reason: {str(e)}.')
        logger.error(message)
