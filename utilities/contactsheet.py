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

        self._cell_w = self._page_w / self._n_cols
        self._cell_h = self._page_h / self._n_rows

        self._next_row = 0
        self._next_col = 0

    def place_cell(self, image_cell):
        print(f'Placing cell...')
        im_path = image_cell.get_image_path()

        page_x = self._get_page_x(self._next_col)
        page_y = self._get_page_y(self._next_row)

        im_height = self._get_im_height(image_cell)
        im_width = self._get_im_width(image_cell)

        self._canvas.drawImage(image=im_path,
                               preserveAspectRatio=True,
                               x=page_x*mm,
                               y=page_y*mm,
                               height=im_height*mm,
                               width=im_width*mm)

        self._update_next_pos()

    def _update_next_pos(self):
        self._next_col += 1
        if self._next_col == self._n_cols:
            self._next_col = 0
            self._next_row += 1

    def is_full(self):
        return self._next_row == self._n_rows

    def _get_page_x(self, col):
        page_x = (self._cell_w * col) 
        return page_x

    def _get_page_y(self, row):
        page_y = (self._cell_h * row) 
        return page_y

    def _get_im_height(self, image_cell):
        return image_cell.get_n_rows() * self._cell_h

    def _get_im_width(self, image_cell):
        return image_cell.get_n_cols() * self._cell_w

    def save(self):
        self._canvas.save()
