from utilities.contactsheet_manager import ContactsheetManager
import os
import utilities.constants as const
from typing import List
# from utilities.image_cell
from utilities.preprocessors.preprocessor import Preprocessor


class BookPart:
    def __init__(self, raw_input_dir, part_name, preprocessor_class) -> None:
        self._raw_input_dir = raw_input_dir
        self.part_name = part_name
        self._assets_dir_name = None
        self._contactsheets_dir_name = None
        self._image_cells_list = []
        self._cs_manager = None

        self._init_part_dirs()
        self._preprocessor: Preprocessor = preprocessor_class(
            self._raw_input_dir, self._assets_dir_name)

    def _get_output_dir_name(self, output_type):
        print(f'Getting {output_type} output dir name...')
        return os.path.join(const.OUTPUTS_PATH, self.part_name, output_type)

    def _init_assets_dir(self):
        print(f'Initing assets dir...')
        self._assets_dir_name = self._get_output_dir_name(
            output_type=const.ASSETS_TYPE)
        os.makedirs(name=self._assets_dir_name,
                    exist_ok=True)

    def _init_contactsheets_dir(self):
        print(f'Initing contactsheets dir...')
        self._contactsheets_dir_name = self._get_output_dir_name(
            output_type=const.CONTACTSHEETS_TYPE)
        os.makedirs(name=self._contactsheets_dir_name,
                    exist_ok=True)

    def _init_part_dirs(self):
        print(f'Initing part dirs...')
        self._init_assets_dir()
        self._init_contactsheets_dir()

    def _preprocess_image(self, input_basename):
        print(f'Preprocessing {input_basename}...')
        self._preprocessor.preprocess(
            input_basename=input_basename)

    def preprocess_inputs(self):
        print(f'Preprocessing inputs for {self.part_name}...')
        for base_fn in sorted(os.listdir(self._raw_input_dir)):
            self._preprocess_image(
                input_basename=base_fn)

    def create_contactsheets(self):
        print(f'Creating contactsheet for {self.part_name}...')
