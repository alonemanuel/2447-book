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
    def preprocess(self, input_basename, big_lines=False):
        super().preprocess(input_basename=input_basename)
        input_fn = os.path.join(self.input_dir, input_basename)
        output_fn = os.path.join(self.output_dir, input_basename)
        # if os.path.isfile(output_fn):
        #     print(f'File os.p{os.path.basename(output_fn)} exists')
        #     return output_fn
        os.makedirs(os.path.dirname(output_fn), exist_ok=True)
        
        print(f'got to prep!!!!!!!!!')

        img = self._get_image(input_fn)
        print(f'got image: {input_fn}')
        edged = self._get_edged_image(image=img,
                                      sigma=2, big_lines=big_lines)


        print(f'outputfn = {output_fn}')
        cv2.imwrite(filename=output_fn, img=edged)
        return output_fn

    def _get_edged_image(self, image, sigma, big_lines=False):
        edged = self._auto_canny(image=image,
                                sigma=sigma, big_lines=big_lines)
                                       # Create a kernel for dilation
        kernel = np.ones((3,3), np.uint8)

        # Apply dilation to thicken the lines
        edged = cv2.dilate(edged, kernel, iterations=1)

        # # Display the image
        # cv2.imshow('Edges', edges)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


        # v = np.median(image)
        # lower = int(max(0, (1.0 - sigma) * v))
        # upper = int(min(255, (1.0 + sigma) * v))
        # edged = cv2.Canny(image, lower, upper)
        edged=cv2.bitwise_not(edged)
        return edged

    def _get_image(self, input_fn):
        return cv2.imread(input_fn, 0)

    def _auto_canny(self, image, sigma, big_lines=False):
        # import cv2
        # import numpy as np

        # Load the image
        # img = cv2.imread('image.jpg',0)

        # Compute the median of the image
        median = np.median(image)

        # Set the lower and upper thresholds as 1.5 times the median value
        if not big_lines:
            sigma = 0.8
        else:
            sigma = 0.7

        lower_threshold = int(max(0, (1.0 - sigma) * median))
        upper_threshold = int(min(255, (1.0 + sigma) * median))


        # Apply Canny edge detection
        edged = cv2.Canny(image, lower_threshold, upper_threshold,L2gradient=False)

         
        return edged
