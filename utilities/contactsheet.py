from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm, inch


class Contactsheet:

    def __init__(self, contactsheet_fn, n_rows, n_cols, page_w, page_h, gap_mm) -> None:
        print('Initing contactsheet...')
        self._n_images_placed = 0
        self._page_w = page_w
        self._page_h = page_h

        self._canvas = canvas.Canvas(filename=contactsheet_fn,
                                     pagesize=(self._page_w*mm, self._page_h*mm))
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._gap_mm = gap_mm

        self._cell_w = self._get_gapped_width()
        self._cell_h = self._page_h / self._n_rows

        self._next_row = 0
        self._next_col = 0

    def _get_gapped_width(self):
        overall_gap_space = self._gap_mm * (self._n_cols - 1)
        overall_left_space = self._page_w - overall_gap_space
        return overall_left_space / self._n_cols

    def _get_gapped_height(self):
        overall_gap_space = self._gap_mm * (self._n_rows - 1)
        overall_left_space = self._page_h - overall_gap_space
        return overall_left_space / self._n_rows

    def place_cell(self, image_cell):
        print(f'Placing cell...')
        im_path = image_cell.get_image_path()

        x = self._get_x(self._next_col)
        y = self._get_y(self._next_row)

        im_height = self._get_im_height(image_cell)
        im_width = self._get_im_width(image_cell)

        self._draw_image(image=im_path,
                         preserveAspectRatio=True,
                         x=x,
                         y=y,
                         height=im_height,
                         width=im_width)

        self._update_next_pos()

    def _draw_image(self, image, preserveAspectRatio, x, y, height, width):
        page_x = self._get_page_x(x, width)
        page_y = self._get_page_y(y, height)
        self._canvas.drawImage(image=image,
                               preserveAspectRatio=preserveAspectRatio,
                               x=page_x*mm,
                               y=page_y*mm,
                               height=height*mm,
                               width=width*mm)

    def _update_next_pos(self):
        self._next_col += 1
        if self._next_col == self._n_cols:
            self._next_col = 0
            self._next_row += 1

    def is_full(self):
        return self._next_row == self._n_rows

    def _get_x(self, col):
        image_offset = self._cell_w * col
        gap_offset = self._gap_mm * col
        return image_offset + gap_offset

    def _get_y(self, row):
        image_offset = self._cell_h * row
        gap_offset = self._gap_mm * row
        return image_offset + gap_offset

    def _get_page_x(self, x, width):
        return self._page_w - x - width

    def _get_page_y(self, y, height):
        return self._page_h - y - height

    def _get_im_height(self, image_cell):
        return image_cell.get_n_rows() * self._cell_h

    def _get_im_width(self, image_cell):

        return image_cell.get_n_cols() * self._cell_w

    def save(self):
        self._canvas.save()
