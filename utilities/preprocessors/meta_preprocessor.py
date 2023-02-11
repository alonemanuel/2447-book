from numpy import array
import numpy as np
import cv2
from utilities.my_svg import MySVG

from utilities.preprocessors.preprocessor import Preprocessor
from PIL import Image
import os
import shutil
import utilities.constants as const
from utilities.my_colorthief import MyColorThief


class MetaPreprocessor(Preprocessor):

    def __init__(self, input_dir, output_dir) -> None:
        super().__init__(input_dir, output_dir)

    def preprocess(self, input_basename):
        super().preprocess(input_basename=input_basename)

        self._input_fn = os.path.join(self.input_dir, input_basename)
        self._output_fn = os.path.join(self.output_dir, self.get_output_fn())
        self._input_image = Image.open(self._input_fn)

        self._palette = self.extract_palette()
        self._faces = self.extract_faces()
        self._text = self.extract_text()

        self._output_svg = MySVG(filename=self.get_output_fn())
        self._output_svg.add_metadata(
            colors_hex=self._palette, faces_im=self._faces, texts_str=[])
        # self._output_svg.add_colorbars(self._palette)
        # if self._faces:
        #     self._output_svg.add_image(self._faces[0])
        return self.save_output()

    def get_output_fn(self):
        basename = os.path.basename(self._input_fn)
        base, ext = os.path.splitext(basename)
        return f'{base}.svg'

    def save_output(self):
        self._output_svg.saveas(dir_path=os.path.split(
            self._output_fn)[0], pretty=True)
        return self._output_fn

    def extract_palette(self):
        color_thief = MyColorThief(self._input_image)
        orig_palette = color_thief.get_palette(
            color_count=const.DEF_PALETTE_SIZE)[:3]
        # print(orig_palette)
        filtered_palette = color_thief.unique_colors(orig_palette, threshold=const.DEF_COLOR_UNIQUE_THRESH)
        return filtered_palette

    def extract_faces(self):
        import cv2

        # Load the cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier(os.path.join('assets',
                                                          'haarcascade_frontalface_alt2.xml'))

        # Load the image
        img = cv2.imread(self._input_fn)

        # Convert the image to grayscale for faster face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        print(f'Found {len(faces)} faces')

        # Loop over the faces and save each face to a separate image file
        face_paths = []
        for (x, y, w, h) in faces:
            face = img[y:y+h, x:x+w]

            face_path = f'face_{x}_{y}.jpeg'
            faces_dir = os.path.join(self.output_dir, 'faces')
            face_abs_path = os.path.join(faces_dir, face_path)
            os.makedirs(faces_dir, exist_ok=True)
            cv2.imwrite(face_abs_path, face)
            face_paths.append(face_abs_path)
        return face_paths[:2]

    def extract_text(self):
        pass

        # input_fn = os.path.join(self.input_dir, input_basename)
        # output_fn = os.path.join(self.output_dir, input_basename)

        # img = self._get_image(input_fn)
        # edged = self._get_edged_image(image=img,
        #                               sigma=999)

        # cv2.imwrite(filename=output_fn, img=edged)
        # return output_fn
