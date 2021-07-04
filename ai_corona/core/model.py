import logging

import os
import re
import cv2
import glob
import numpy as np
import pydicom as dcm

from tensorflow.keras.applications.densenet import preprocess_input
from tensorflow.keras.layers import Input
from tensorflow.keras.models import load_model

from ai_corona.core.efficientnet.tfkeras import EfficientNetB3

logger = logging.getLogger('backend')

MODEL_PATH = f'{os.getcwd()}/ai_corona/core/h5s/ai_corona.h5'

# Move these guys to a dedicated file.
BATCH_SIZE = 8
SHAPE = 512


class COVID19DiagnosisModel:
    def __init__(self) -> None:
        logger.info('Initializing COVID-19 diagnosis model...')
        try:
            self.batch_size = BATCH_SIZE
            self.shape = SHAPE
            self.img_input = Input(shape=(SHAPE, SHAPE, 3))
            self.efficient_net_b3 = EfficientNetB3(include_top=False,
                                                   input_shape=(self.shape,
                                                                self.shape, 3),
                                                   input_tensor=self.img_input,
                                                   weights='imagenet',
                                                   classes=14,
                                                   pooling='avg')
            self.model = load_model(MODEL_PATH)

            self.case_path = None
            self.features = None

            logger.info('COVID-19 diagnosis model initialized!')
        except Exception as e:
            message = ('Failed to initialize COVID-19 diagnosis model. '
                       f'Reason: {str(e)}.')
            logger.error(message)
            raise Exception(message)  # todo: Replace base exception.

    def run(self, case_directory_path):
        self.case_path = case_directory_path
        return self.__run_diagnosis()

    def __run_diagnosis(self):
        logger.info('Running diagnosis...')

        ls_dire = glob.glob(self.case_path + '/*.dcm')
        ls_dire = [[s, int(re.findall(r'\d+', s)[-1])] for s in ls_dire]
        ls_dire = sorted(ls_dire, key=lambda x: x[1])

        if len(ls_dire) == 0:
            ls_dire = glob.glob(self.case_path + '/*.DCM')
            ls_dire = [[s, int(re.findall(r'\d+', s)[-1])] for s in ls_dire]
            ls_dire = sorted(ls_dire, key=lambda x: x[1])

        ls_dire = np.array(ls_dire)[:, 0]

        ct_data = []
        for s in ls_dire:
            slice_0 = dcm.dcmread(s)
            slice_0 = np.array(slice_0.pixel_array, float)
            ct_data.append(cv2.resize(slice_0, (512, 512)))
        ct_data = np.array(ct_data)
        ct_data = self.window(ct_data)

        p = self.efficient_net_b3.predict(preprocess_input(ct_data),
                                          batch_size=self.batch_size)

        k = 0.5
        x = len(p)
        ss = int(len(p) * k)

        p = np.mean(p[int((x - ss) / 2) + 1:-int((x - ss) / 2) + 1], axis=0)
        prediction = np.round(
            self.model.predict(np.expand_dims(p, axis=0))[0], 4) * 100

        logger.info('Diagnosis complete!')

        return list(prediction)

    @staticmethod
    def window(img: np.ndarray) -> np.ndarray:
        WL, WW = -600, 1500
        upper, lower = WL + WW // 2, WL - WW // 2
        X = np.clip(img.copy(), lower, upper)
        X = X - np.min(X)
        X = X / (np.max(X) / 255.0)
        X = X.astype('uint8')
        X = np.expand_dims(X, axis=-1)
        X = np.concatenate([X, X, X], axis=-1)
        return X
