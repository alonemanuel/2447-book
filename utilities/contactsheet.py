from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm, inch
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import utilities.constants as const


class Contactsheet:

    def __init__(self, contactsheet_fn, n_rows, n_cols, page_w, page_h, row_gap, col_gap) -> None:
        print('Initing contactsheet...')
        self._n_images_placed = 0
        self._page_w = page_w
        self._page_h = page_h

        self._canvas = canvas.Canvas(filename=contactsheet_fn,
                                     pagesize=(self._page_w*mm, self._page_h*mm))
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._row_gap = row_gap
        self._col_gap = col_gap

        self._cell_w = self._get_gapped_width()
        self._cell_h = self._get_gapped_height()

        self._next_row = 0
        self._next_col = 0

        self.tag_height_mm = const.DEF_TAG_NUDGE

    def _get_gapped_width(self):
        overall_gap_space = self._col_gap * (self._n_cols - 1)
        overall_left_space = self._page_w - overall_gap_space
        return overall_left_space / self._n_cols

    def _get_gapped_height(self):
        overall_gap_space = self._row_gap * (self._n_rows - 1)
        overall_left_space = self._page_h - overall_gap_space
        return overall_left_space / self._n_rows

    def place_cell(self, image_cell):
        im_path = image_cell.get_image_path()
        print(f'in cs impath: {im_path}')
        image_basename = os.path.basename(im_path)
        image_tag = os.path.splitext(image_basename)[0]
        # print(f'Placing cell {image_tag}...')

        x = self._get_x(self._next_col)
        y = self._get_y(self._next_row)

        im_height = self._get_im_height(image_cell)
        im_width = self._get_im_width(image_cell)

        if image_basename == '0049.png':
            print('EBRRRRRRRRRRRRRRRRRR')
            print(image_cell.get_sizer_type())

        if not image_cell.get_sizer_type() in {const.MEDIUM_CELLED, const.SINGLE_PAGE_CELLED, const.DOUBLE_PAGE_CELLED}:
            print(f'im path: {im_path}')
            self._draw_image(image=im_path,
                             preserveAspectRatio=True,
                             x=x,
                             y=y,
                             height=im_height,
                             width=im_width)
        else:
            print('ENTERED CLAUYSE')

        self._draw_tagline(tag=image_tag,
                           row=self._next_row,
                           col=self._next_col,
                           im_height=im_height)

        self._update_next_pos()

    def _draw_tagline(self, tag, row, col, im_height):
        tag_x = (self._get_x(col) + self._cell_w/2)
        tag_y = (self._get_y(row) + im_height) + const.DEF_TAG_GAP
        page_x = self._get_page_x(tag_x, 0)
        page_y = self._get_page_y(tag_y, 0)

        self._canvas.saveState()
        self._canvas.setFont(const.DIATYPE_FONT_NAME, const.DEF_FONT_TAG_SIZE)
        self._canvas.drawCentredString(page_x, page_y, tag)
        self._canvas.restoreState()

        # textobj = self._canvas.beginText(page_x, page_y)

    def _draw_image(self, image, preserveAspectRatio, x, y, height, width):
        page_x = self._get_page_x(x, width)
        page_y = self._get_page_y(y, height)

        print(f'image: {image}')


        if 'svg' in os.path.splitext(os.path.basename(image))[1]:
            page_y = self._get_svg_page_y(y, height)
            print(f'is svg')
            drawing = svg2rlg(image)
            renderPDF.draw(drawing, self._canvas, x=page_x,
                           y=page_y)
        else:
            self._canvas.drawImage(image=image,
                                   preserveAspectRatio=preserveAspectRatio,
                                   x=page_x,
                                   y=page_y,
                                   height=height*mm,
                                   width=width*mm,
                                   anchor=const.DEF_CS_ANCHOR)

    def _update_next_pos(self):
        self._next_col += 1
        if self._next_col == self._n_cols:
            self._next_col = 0
            self._next_row += 1

    def is_full(self):
        return self._next_row == self._n_rows

    def _get_x(self, col):
        image_offset = self._cell_w * col
        gap_offset = self._col_gap * col
        return image_offset + gap_offset

    def _get_y(self, row):
        image_offset = self._cell_h * row
        gap_offset = self._row_gap * row
        return image_offset + gap_offset

    def _get_page_x(self, x, width):
        return (self._page_w - x - width) * mm

    def _get_page_y(self, y, height):
        return (self._page_h - y - height)*mm
    
    def _get_svg_page_y(self, y, height):
        return (self._page_h - y)*mm

    def _get_im_height(self, image_cell):
        return (image_cell.get_n_rows() * self._cell_h) - self.tag_height_mm

    def _get_im_width(self, image_cell):

        return image_cell.get_n_cols() * self._cell_w

    def save(self):
        self._canvas.save()
