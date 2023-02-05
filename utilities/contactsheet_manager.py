import os
from enum import Enum
from utilities.image_cell import ImageCell
from typing import List
from utilities.contactsheet import Contactsheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import utilities.constants as const


class ContactsheetManager:
    def __init__(self, im_cells_list: List[ImageCell], output_parent_dir,
                 n_rows, n_cols, page_w, page_h, gap_mm):
        self._image_cells_list = im_cells_list
        self._output_parent_dir = output_parent_dir

        self._n_rows = n_rows
        self._n_cols = n_cols

        self._page_w = page_w
        self._page_h = page_h
        self._gap_mm = gap_mm

        self._canvases = []

        self._init_font()

    def _init_font(self):
        pdfmetrics.registerFont(
            TTFont(const.DIATYPE_FONT_NAME, const.DIATYPE_FONT_PATH))



    def create_contactsheets(self, input_dir, output_dir):
        print(f'\nCreating contactsheets...')

        image_counter = 0
        page_counter = 0

        while True:
            print(f'Creating contactsheet no. {page_counter}...')
            cs_fn = self._get_contacsheet_fn(page_counter)
            current_cs = Contactsheet(contactsheet_fn=cs_fn,
                                      n_rows=self._n_rows,
                                      n_cols=self._n_cols,
                                      page_w=self._page_w,
                                      page_h=self._page_h,
                                      gap_mm=self._gap_mm)
            while not current_cs.is_full():
                current_cs.place_cell(self._image_cells_list[image_counter])
                image_counter += 1
                if image_counter == len(self._image_cells_list):
                    current_cs.save()
                    return
            current_cs.save()
            page_counter += 1


    def _get_page_x(self, right_col):
        pass
    def _get_page_y(self, top_row):
        pass

    def _get_contacsheet_fn(self, page_counter):
        return os.path.join(self._output_parent_dir, f'cs_{page_counter:02d}.pdf')

