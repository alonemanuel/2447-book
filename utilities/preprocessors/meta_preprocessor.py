from numpy import array
import numpy as np
import cv2
from utilities.my_svg import MySVG
import imutils
from utilities.preprocessors.preprocessor import Preprocessor
from PIL import Image
import os
import shutil
import utilities.constants as const
from utilities.my_colorthief import MyColorThief
import pytesseract


class MetaPreprocessor(Preprocessor):

    def __init__(self, input_dir, output_dir) -> None:
        super().__init__(input_dir, output_dir)

    def preprocess(self, input_basename):
        super().preprocess(input_basename)
        self._input_fn = os.path.join(self.input_dir, input_basename)
        output_fn_orig_ext = os.path.join(self.output_dir, self.get_output_fn())
        output_fn_no_ext = os.path.splitext(output_fn_orig_ext)[0]
        output_fn_jpg_ext = f'{output_fn_no_ext}.jpg'
        self._output_fn = output_fn_jpg_ext
        if os.path.isfile(self._output_fn):
            print(f'File os.p{os.path.basename(self._output_fn)} exists')
            return self._output_fn

        # self._input_image = Image.open(self._input_fn)
        self._input_image = cv2.imread(self._input_fn)

        # self.output_dir =
        # os.makedirs()
        

        face = self.save_face_to_file(input_basename)
        # text = self.save_text_to_file(input_basename)

        # self._palette = self.extract_palette()
        # self._faces = self.extract_faces()
        # self._text = self.extract_text()

        # self._output_svg = MySVG(filename=self.get_output_fn())
        # self._output_svg.add_metadata(
        #     colors_hex=self._palette, faces_im=self._faces, texts_str=[])
        # # self._output_svg.add_colorbars(self._palette)
        # # if self._faces:
        # #     self._output_svg.add_image(self._faces[0])
        # if text:
        #     print(f'Found text: f{text}')
        if face is not None:
            print('found face')
            cv2.imwrite(filename=self._output_fn, img=face)

            return self._output_fn
        else:
            image = np.full((16, 16), 255, dtype=np.uint8)
            cv2.imwrite(filename=self._output_fn, img=image)

    def save_text_to_file(self, input_basename):
        # self._input_image = Image.open(self._input_fn)
        img = cv2.resize(self._input_image, (620,480))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
        gray = cv2.bilateralFilter(gray, 11, 17, 17)

        # cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = imutils.grab_contours(cnts)
        # cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
        # screenCnt = None

        # # loop over our contours
        # for c in cnts:
        #                 # approximate the contour
        #                 peri = cv2.arcLength(c, True)
        #                 approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        #                 # if our approximated contour has four points, then
        #                 # we can assume that we have found our screen
        #                 if len(approx) == 4:
        #                     screenCnt = approx
        #                     break

        # # Masking the part other than the number plate
        # mask = np.zeros(gray.shape,np.uint8)
        # new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
        # new_image = cv2.bitwise_and(img,img,mask=mask)

        # # Now crop
        # (x, y) = np.where(mask == 255)
        # (topx, topy) = (np.min(x), np.min(y))
        # (bottomx, bottomy) = (np.max(x), np.max(y))
        # Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        #Read the number plate

        # img = Image.open('mIjNm.png')
        self._input_image = Image.fromarray(gray)
        text = pytesseract.image_to_string(self._input_image)
        # text = text.replace('\n', '').replace('\f', '')
        if text:
            txt_basename = f'{os.path.splitext(input_basename)[0]}.txt'
            output_text_fn = os.path.join(self.output_dir, 'texts',txt_basename)
            with open(output_text_fn, 'w') as f:
                f.write(text)


    def save_face_to_file(self, input_basename):
        # self._input_fn = os.path.join(self.input_dir, input_basename)
        # self._output_fn = os.path.join(self.output_dir, self.get_output_fn())

        
        import cv2


        # Load the pre-trained face detection model
        model = cv2.dnn.readNetFromCaffe(const.DEPLOY_FN, const.CAFFE_MODEL)

        # Load the input image

        # Perform face detection on the input image
        (h, w) = self._input_image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(self._input_image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        model.setInput(blob)
        detections = model.forward()

        # Set a confidence threshold for face detection
        confidence_threshold = 0.5

        # Loop over the detected faces and filter out non-faces based on the
        # confidence score

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > confidence_threshold:
                # Extract the coordinates of the detected face region
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Extract the face from the input image
                face = self._input_image[startY:endY, startX:endX]
                return face

                # Save the detected face
                # cv2.imwrite(f'face_{i}.jpg', face)


    def old_preprocess(self, input_basename):
        super().preprocess(input_basename=input_basename)

        self._input_fn = os.path.join(self.input_dir, input_basename)
        self._output_fn = os.path.join(self.output_dir, self.get_output_fn())
        if os.path.isfile(self._output_fn):
            print(f'File os.p{os.path.basename(self._output_fn)} exists')
            return self._output_fn

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
        # print(f'Found {len(faces)} faces')

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
