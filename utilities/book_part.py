from utilities.contactsheet_manager import ContactsheetManager
import os
import utilities.constants as const
from typing import List
from utilities.image_cell import ImageCell
from utilities.preprocessors.preprocessor import Preprocessor


class BookPart:
    def __init__(self, raw_input_dir, part_name, preprocessor_class, cs_n_rows,
                 cs_n_cols, row_gap, col_gap, is_batched=False, image_limit=3000) -> None:
        print(f'Initing book part: {part_name}')
        self._raw_input_dir = raw_input_dir
        self.part_name = part_name
        self._assets_dir_name = None
        self._contactsheets_dir_name = None

        self._image_limit = image_limit
        
        self._is_batched = is_batched

        self._medium_sized = []
        self._single_page_sized = []
        self._double_page_sized = []

        self._row_gap = row_gap
        self._col_gap = col_gap

        # self._init_special_images()

        self._image_cells_list = []

        self._init_part_dirs()
        self._preprocessor: Preprocessor = preprocessor_class(
            self._raw_input_dir, self._assets_dir_name)

        self._cs_manager = ContactsheetManager(im_cells_list=self._image_cells_list,
                                               output_parent_dir=self._contactsheets_dir_name,
                                               n_rows=cs_n_rows,
                                               n_cols=cs_n_cols,
                                               page_w=const.PAGE_W,
                                               page_h=const.PAGE_H,
                                               row_gap=self._row_gap,
                                               col_gap=self._col_gap
                                               )

    def _init_special_images(self):
        for fn in os.listdir(const.MEDIUM_STILLS_PATH):
            self._medium_sized.append(fn)
        for fn in os.listdir(const.SINGLE_PAGE_STILLS_PATH):
            self._single_page_sized.append(fn)
        for fn in os.listdir(const.DOUBLE_PAGE_STILLS_PATH):
            self._double_page_sized.append(fn)

        print(f'medium: {self._medium_sized}')
        print(f'single page: {self._single_page_sized}')
        print(f'double: {self._double_page_sized}')

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
        processed_fn = self._preprocessor.preprocess(
            input_basename=input_basename)
        return processed_fn

    def preprocess_inputs(self):
        print(f'Preprocessing inputs for {self.part_name}...')
        if self._is_batched:
            self.preprocess_batched()
            return
        
        for i, base_fn in enumerate(sorted(os.listdir(self._raw_input_dir))):
            if i >= self._image_limit:
                return
            processed_fn = self._preprocess_image(
                input_basename=base_fn)
            cell_sizer = self._get_cell_sizer(base_fn)

            print(f'processed fn: {processed_fn}')
            self._image_cells_list.append(
                ImageCell(processed_fn, cell_sizer=cell_sizer))

    def preprocess_batched(self):
        image_count = 0
        for i, batch_dir in enumerate(sorted(os.listdir(self._raw_input_dir))):
            if image_count >= self._image_limit:
                return
            batch_dir_abs = os.path.join(self._raw_input_dir, batch_dir)
            for j, file_name in enumerate(sorted(os.listdir(batch_dir_abs))):
                fn_abs = os.path.join(batch_dir, file_name)
                print(f'working on: {fn_abs}')
                processed_fn = self._preprocess_image(
                    input_basename=fn_abs)
                # cell_sizer = self._get_cell_sizer(batch_dir)
                print(f'pro fn: {processed_fn}')
                
                self._image_cells_list.append(
                    ImageCell(processed_fn, cell_sizer=const.SINGLE_CELLED))





    def _get_cell_sizer(self, base_fn):
        cell_sizer = const.SINGLE_CELLED
        # print(f'base fn: {base_fn}')
        if base_fn in self._medium_sized:
            print('in medium')
            cell_sizer = const.MEDIUM_CELLED
        elif base_fn in self._single_page_sized:
            print('in single')
            cell_sizer = const.SINGLE_PAGE_CELLED
        elif base_fn in self._double_page_sized:
            print('in double')
            cell_sizer = const.DOUBLE_PAGE_CELLED
        return cell_sizer

    def _init_image_cells(self):
        for fn in sorted(os.listdir(self._assets_dir_name)):
            full_fn = os.path.join(self._assets_dir_name, fn)
            cell_sizer = self._get_cell_sizer(fn)
            self._image_cells_list.append(
                ImageCell(full_fn, cell_sizer=cell_sizer))

    def _init_batched_image_cells(self):
        print(f'Initing batched cells...')
        for dir in sorted(os.listdir(self._assets_dir_name)):
            dir_path = os.path.join(self._assets_dir_name, dir)
            if os.path.isdir(dir_path):
                print(f'Found dir: {dir}')
                new_list = []
                self._image_cells_list.append(new_list)
                for fn in sorted(os.listdir(dir_path)):
                    fn_path = os.path.join(dir_path, fn)
                    cell_sizer = self._get_cell_sizer(fn)
                    new_list.append(
                        ImageCell(fn_path, cell_sizer=cell_sizer))

    def create_batched_contactsheets(self, row_start, col_start):
        self._init_batched_image_cells()
        self._cs_manager.create_batched_contactsheets(row_start=row_start, col_start=col_start)

    def create_contactsheets(self, image_limit, row_start=0, col_start=0):
        if self._is_batched:
            self.create_batched_contactsheets(row_start, col_start)
            return
        if not self._image_cells_list:
            self._init_image_cells()
        self._cs_manager.create_contactsheets(image_limit=image_limit)
