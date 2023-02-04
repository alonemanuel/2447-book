import os
from enum import Enum
from utilities.image_cell import ImageCell
from typing import List


class ContactsheetManager:
    def __init__(self, im_cells_list: List[ImageCell], output_parent_dir):
        self._image_cells_list = im_cells_list

    
    def create_contactsheets(self):
        print(f'Creating contactsheets...')

        image_counter = 0
        page_counter = 0

        for i, image_cell in enumerate(self._image_cells_list):
            print(f'Creating contactsheet no. {i}...')
