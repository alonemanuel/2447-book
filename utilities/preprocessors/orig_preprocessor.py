from utilities.preprocessors.preprocessor import Preprocessor
from PIL import Image
import os
import shutil

class OrigPreprocessor(Preprocessor):
    


    def preprocess(self, input_basename) -> Image:
        super().preprocess(input_basename)
        input_fn = os.path.join(self.input_dir, input_basename)
        output_fn = os.path.join(self.output_dir, input_basename)
        shutil.copy(input_fn, output_fn)
        return output_fn
