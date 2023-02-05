import os
from enum import Enum
from utilities.image_cell import ImageCell
from typing import List
from utilities.contactsheet import Contactsheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import utilities.constants as const


class ContactsheetManager:
    def __init__(self, im_cells_list, output_parent_dir,
                 n_rows, n_cols, page_w, page_h, row_gap, col_gap):
        self._image_cells_list = im_cells_list
        self._output_parent_dir = output_parent_dir

        self._n_rows = n_rows
        self._n_cols = n_cols

        self._page_w = page_w
        self._page_h = page_h
        self._row_gap_mm = row_gap
        self._col_gap_mm = col_gap

        self._canvases = []

        self._init_font()

    def _init_font(self):
        pdfmetrics.registerFont(
            TTFont(const.DIATYPE_FONT_NAME, const.DIATYPE_FONT_PATH))

    def create_batched_contactsheets(self):
        print(f'\nCreating contactsheets...')

        dir_counter = 0
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
                                      row_gap=self._row_gap_mm,
                                      col_gap=self._col_gap_mm)

            while not current_cs.is_full():
                curr_dir = self._image_cells_list[dir_counter]
                current_cs.place_cell(curr_dir[image_counter])
                image_counter += 1
                if image_counter == len(curr_dir):
                    image_counter = 0
                    dir_counter += 1
                    if dir_counter == len(self._image_cells_list):
                        current_cs.save()
                        return
            current_cs.save()
            page_counter += 1

    def create_contactsheets(self):
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
