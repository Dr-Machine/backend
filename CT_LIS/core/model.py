import logging

import os

import cv2
import numpy as np
from PIL import Image

import SimpleITK as sitk
from lungmask import mask as msk
from skimage import measure

from tensorflow.keras.models import load_model

from scipy.ndimage import gaussian_filter as gf
from scipy.ndimage.morphology import binary_dilation

logger = logging.getLogger('backend')

MODEL_PATH = f'{os.getcwd()}/CT_LIS/core/h5s/fuck_model.h5'
WEIGHTS_0_PATH = f'{os.getcwd()}/CT_LIS/core/h5s/weight_0.h5'
WEIGHTS_1_PATH = f'{os.getcwd()}/CT_LIS/core/h5s/weight_1.h5'

BATCH_SIZE = 8


class CTLungInfectionSegmentationModel:
    def __init__(self) -> None:
        logger.info('Initializing CT lung infection segmentation model...')
        try:
            self.batch_size = BATCH_SIZE

            # todo: run msk on mock data for init
            self.msk = msk
            self.model = load_model(MODEL_PATH)

            self.case_path = None
            self.result_path = None

            self.image3D = None
            self.lobe_segmentation = None
            self.infection_segmentation = None
            self.features = None

            logger.info('CT lung infection segmentation model initialized!')
        except Exception as e:
            message = ('Failed to initialize CT lung infection segmentation '
                       f'model. Reason: {str(e)}.')
            logger.error(message)
            raise Exception(message)  # todo: Replace base exception.

    def run(self, case_directory_path, result_directory_path):
        self.case_path = case_directory_path
        self.result_path = result_directory_path
        return self.__run_segmentation()

    def __run_segmentation(self):
        logger.info('Running segmentation...')

        series_IDs = self.__extract_series_ids()

        series_file_names = self.__extract_series_filenames(
            series_IDs=series_IDs)

        series_reader = self.__read_series(series_file_names=series_file_names)
        self.image3D = self.__execute_series_reader(series_reader)

        # self.lobe_segmentation = self.__run_mask()
        self.lobe_segmentation = np.load('ls.npy')

        self.image3D = self.__preprocess()

        # self.infection_segmentation = self.__run_models()
        self.infection_segmentation = np.load('is.npy')

        features = []
        for i_lobe in range(1, 6):
            lobe_point = self.infection_segmentation.copy()
            lobe_point = lobe_point[self.lobe_segmentation == i_lobe]
            lobe_point = lobe_point.flatten()
            features.append(((lobe_point > 0.5).sum()) / len(lobe_point))

        features = np.round(np.array(features) * 100, 1)
        self.features = features

        logger.info('Segmentation complete!')
        logger.info(f'Extracted features: {self.features}')

        self.__store_results()

        return list(self.features)

    def __extract_series_ids(self):
        logger.info('Extracting series IDs...')
        try:
            series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(
                self.case_path)
            logger.info('Series IDs extracted!')
            return series_IDs
        except Exception as e:
            message = (f'Failed to extract series IDs. Reason: {str(e)}.')
            logger.error(message)

    def __extract_series_filenames(self, series_IDs):
        logger.info('Extracting series filenames...')
        try:
            series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(
                self.case_path, series_IDs[0])
            logger.info('Series filenames extracted!')
            return series_file_names
        except Exception as e:
            message = (
                f'Failed to extract series filenames. Reason: {str(e)}.')
            logger.error(message)

    def __run_mask(self):
        logger.info('Running mask...')
        try:
            _mask = self.msk.apply_fused(self.image3D,
                                         basemodel='LTRCLobes',
                                         fillmodel='R231',
                                         force_cpu=False,
                                         batch_size=8,
                                         volume_postprocessing=True,
                                         noHU=False)
            logger.info('Mask run complete!')
            return _mask
        except Exception as e:
            message = (f'Failed to run mask. Reason: {str(e)}.')
            logger.error(message)

    def __preprocess(self):
        logger.info('Pre-processing...')
        try:
            sss = 0.7
            ct = sitk.GetArrayViewFromImage(self.image3D).copy()
            ct[ct < -1024] = -1024
            sig = min((ct.shape[2] / 150.) * sss, 1)
            ct = gf(ct, sig)
            ct = self.__calculate_window(ct)
            ct = np.array([ct, ct, ct]).transpose(1, 2, 3, 0)
            logger.info('Pre-process complete!')
            return ct
        except Exception as e:
            message = (f'Failed to pre-process. Reason: {str(e)}.')
            logger.error(message)

    def __run_models(self):
        logger.info('Running models...')
        try:
            aggregate = self.__run_model_0() + self.__run_model_1()
            logger.info('Model runs complete!')
            return aggregate
        except Exception as e:
            message = (f'Failed to run models. Reason: {str(e)}.')
            logger.error(message)

    def __run_model_0(self):
        logger.info('Running model_0...')
        try:
            self.model.load_weights(WEIGHTS_0_PATH)
            infection_segmentation = (self.model.predict(
                self.image3D[:, :, ::-1, :],
                batch_size=self.batch_size,
                workers=16,
                verbose=1)[:, :, ::-1, 0] + self.model.predict(
                    self.image3D, batch_size=self.batch_size,
                    workers=16)[:, :, :, 0]) / 2
            logger.info('Model_0 run complete!')
            return infection_segmentation
        except Exception as e:
            message = (f'Failed to run model_0. Reason: {str(e)}.')
            logger.error(message)

    def __run_model_1(self):
        logger.info('Running model_1...')
        try:
            self.model.load_weights(WEIGHTS_1_PATH)
            infection_segmentation = (self.model.predict(
                self.image3D[:, :, ::-1, :],
                batch_size=self.batch_size,
                workers=16,
                verbose=1)[:, :, ::-1, 0] + self.model.predict(
                    self.image3D, batch_size=self.batch_size,
                    workers=16)[:, :, :, 0]) / 2
            logger.info('Model_1 run complete!')
            return infection_segmentation
        except Exception as e:
            message = (f'Failed to run model_1. Reason: {str(e)}.')
            logger.error(message)

    def __store_results(self):
        logger.info('Storing results...')
        try:
            for s in range(len(self.infection_segmentation)):
                a = self.__plot_slice(s=s)
                a = Image.fromarray(a)
                a.save(self.result_path + str(s).zfill(3) + '.jpg',
                       format='JPEG',
                       quality=80)
            logger.info('Results stored!')
        except Exception as e:
            message = (f'Failed to store results. Reason: {str(e)}.')
            logger.error(message)

    def __plot_slice(self, s):
        try:
            nii_data = self.image3D[:, :, :, 0].astype('uint8')
            nii_mask = self.infection_segmentation > 0.5
            contour = measure.find_contours(nii_mask[s, :, :], 0.5)

            rgb_img = cv2.merge(
                [nii_data[s, :, :], nii_data[s, :, :], nii_data[s, :, :]])

            font = cv2.FONT_HERSHEY_SIMPLEX
            main0 = rgb_img.copy()

            for t in range(len(contour)):
                i = np.array(np.round(contour[t], 0), int)
                img_pl = np.zeros((512, 512))
                cv2.fillPoly(img_pl, pts=[i[:, [1, 0]]], color=(1))
                img_pl = np.array(img_pl)
                img_pl[img_pl > 0] = 1
                img_pl = binary_dilation(img_pl,
                                         structure=np.ones((3, 3)),
                                         iterations=1)

                contour_2 = measure.find_contours(img_pl, 0.5)
                i2 = np.array(np.round(contour_2[0], 0), int)
                cv2.drawContours(rgb_img, [i2[:, [1, 0]]], -1, (255, 0, 0), 1)

            main = rgb_img.copy()

            if nii_mask[s, :, :].sum() > 0:
                cv2.putText(main0, 'YES', (5, 50), font, 2, (0, 255, 0), 2,
                            cv2.LINE_AA)
            else:
                cv2.putText(main0, 'No', (5, 50), font, 2, (255, 0, 0), 2,
                            cv2.LINE_AA)

            cv2.putText(main0, str(s), (450, 30), font, 1, (0, 0, 255), 2,
                        cv2.LINE_AA)

            RGBforLabel = {
                1: (0, 0, 204),
                2: (255, 77, 255),
                3: (255, 255, 25),
                4: (0, 255, 255),
                5: (255, 102, 25)
            }

            lobe_name = [
                'Left  Upper', 'Left  Lower', 'Right Upper', 'Right Middle',
                'Right Lower'
            ]

            for i_lobe in range(1, 6):
                seg = (self.lobe_segmentation[s] == i_lobe).astype('uint8')

                contours, _ = cv2.findContours(seg, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)

                for i, c in enumerate(contours):
                    mask = np.zeros(seg.shape, np.uint8)
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    label = i_lobe
                    colour = RGBforLabel.get(label)
                    cv2.drawContours(main, [c], -1, colour, 1)

                colour = RGBforLabel.get(i_lobe)

                cv2.putText(
                    main,
                    lobe_name[i_lobe - 1] + f' = {self.features[i_lobe-1]}%',
                    (5, -5 + i_lobe * 20), font, 0.5, colour, 1, cv2.LINE_AA)

            cv2.putText(main, 'Infection', (370, 25), font, 1, (255, 0, 0), 1,
                        cv2.LINE_AA)

            final_plot = np.concatenate((main0, main), axis=1)

            return final_plot
        except Exception as e:
            message = (f'Failed to plot slice. Reason: {str(e)}.')
            logger.error(message)

    @staticmethod
    def __read_series(series_file_names):
        logger.info('Attempting to read series...')
        try:
            series_reader = sitk.ImageSeriesReader()
            series_reader.SetFileNames(series_file_names)
            series_reader.LoadPrivateTagsOn()
            logger.info('Series read!')
            return series_reader
        except Exception as e:
            message = (f'Failed to read series. Reason: {str(e)}.')
            logger.error(message)

    @staticmethod
    def __execute_series_reader(series_reader):
        logger.info('Executing series reader...')
        try:
            image3D = series_reader.Execute()
            logger.info('Series reader executed!')
            return image3D
        except Exception as e:
            message = (f'Failed to execute series reader. Reason: {str(e)}.')
            logger.error(message)

    @staticmethod
    def __calculate_window(img, WL=-600, WW=1500):
        logger.info('Calculating window...')
        try:
            upper, lower = WL + WW // 2, WL - WW // 2
            X = np.clip(img.copy(), lower, upper)
            X = X - np.min(X)
            X = X / (np.max(X) / 255.0)
            logger.info('Window calculated!')
            return X
        except Exception as e:
            message = (f'Failed to calculate window. Reason: {str(e)}.')
            logger.error(message)
