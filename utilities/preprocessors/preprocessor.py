from abc import ABC, abstractmethod
from PIL import Image
import os


class Preprocessor(ABC):

    def __init__(self, input_dir, output_dir) -> None:
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir

    @abstractmethod
    def preprocess(self, input_basename):
        pass
        # print(
        #     f'Input dir: {self.input_dir}\nOutput dir: {self.output_dir}\nBasename: {input_basename}')

    def get_output_fn(self):
        return os.path.join()
