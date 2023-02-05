from numpy import array
import numpy as np
import cv2
from utilities.preprocessors.preprocessor import Preprocessor
from PIL import Image
import os
import shutil
import utilities.constants as const


class EdgedPreprocessor(Preprocessor):
    # 
    def preprocess(self, input_basename) -> Image:
        super().preprocess(input_basename=input_basename)
        input_fn = os.path.join(self.input_dir, input_basename)
        output_fn = os.path.join(self.output_dir, input_basename)

        img = self._get_image(input_fn)
        edged = self._get_edged_image(image=img,
                                      sigma=999)

        cv2.imwrite(filename=output_fn, img=edged)
        return output_fn

    def _get_edged_image(self, image, sigma):
        return self._auto_canny(image=image,
                                sigma=sigma)

    def _get_image(self, input_fn):
        return cv2.imread(input_fn)

    def _auto_canny(self, image, sigma):
        v = np.median(image)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
        return edged
