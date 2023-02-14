from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm, inch
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import utilities.constants as const


class Contactsheet:

    def __init__(self, contactsheet_fn, n_rows, n_cols, page_w, page_h, row_gap, col_gap,special_images_list , is_svg=False) -> None:
        print('Initing contactsheet...')

        self._special_images_list = special_images_list
        self._n_images_placed = 0
        self._page_w = page_w
        self._page_h = page_h

        self._canvas = canvas.Canvas(filename=contactsheet_fn,
                                     pagesize=(self._page_w*mm, self._page_h*mm))

        # if (is_svg):
        #     self.init_as_svg_cs()
        #     return

        self._n_rows = n_rows
        self._n_cols = n_cols
        self._row_gap = row_gap
        self._col_gap = col_gap

        self._cell_w = self._get_gapped_width()
        self._cell_h = self._get_gapped_height()

        # print(f'cell w: {self._cell_w}, cell h: {self._cell_h}')

        self._next_row = 0
        self._next_col = 0

        self.tag_height_mm = const.DEF_TAG_NUDGE

    def set_next_row_col(self, row, col):
        self._next_row = row
        self._next_col = col

    def _get_gapped_width(self):
        overall_gap_space = self._col_gap * (self._n_cols - 1)
        overall_left_space = self._page_w - overall_gap_space
        return overall_left_space / self._n_cols

    def _get_gapped_height(self):
        overall_gap_space = self._row_gap * (self._n_rows - 1)
        overall_left_space = self._page_h - overall_gap_space
        return overall_left_space / self._n_rows

    def place_cell(self, image_cell, is_batched=False):


        im_path = image_cell.get_image_path()
        # print(f'in cs impath: {im_path}')
        image_tag = image_cell.get_image_tag()
        # print(f'Placing cell {image_tag}...')

        x = self._get_x(self._next_col)
        y = self._get_y(self._next_row)

        im_height = self._get_im_height(image_cell)
        im_width = self._get_im_width(image_cell)

        # if not image_cell.get_sizer_type() in {const.MEDIUM_CELLED, const.SINGLE_PAGE_CELLED, const.DOUBLE_PAGE_CELLED}:
            # print(f'im path: {im_path}')
        self._draw_image(image=im_path,
                            preserveAspectRatio=True,
                            x=x,
                            y=y,
                            height=im_height,
                            width=im_width)
        
        self._draw_ocr(image_tag=image_tag,
                            x=x,
                            y=y,
                            height=im_height,
                            width=im_width)
        # else:
        #     print('ENTERED CLAUYSE')

        if not is_batched or ('_0' in image_tag):
            image_tag = image_tag.replace('_0', '')
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
        self._canvas.setFont(const.EDITORIAL_FONT_NAME, const.DEF_FONT_TAG_SIZE)
        # self._canvas.setFont(const.EDITORIAL_FONT_PATH, const.DEF_FONT_TAG_SIZE)
        self._canvas.drawCentredString(page_x, page_y, tag)
        self._canvas.restoreState()

        # textobj = self._canvas.beginText(page_x, page_y)

    def _draw_ocr(self, image_tag, x, y, height, width):
        # if 'svg' in os.path.splitext(os.path.basename(image))[1]:
        #     self.draw_svg()
        #     return

        page_x = self._get_page_x(x, width)
        page_y = self._get_page_y(y, height)

        # print(f'image: {image}')
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.pdfgen import canvas
        from reportlab.lib.colors import Color, black, blue, red
        from reportlab.lib.enums import TA_CENTER
        from reportlab.platypus.flowables import TopPadder



        from reportlab.platypus import Frame, Paragraph

        # Define the size and position of the text box
        # x = 1 * inch
        # y = 1 * inch
        # width = 4 * inch
        # height = 3 * inch

        # Create a canvas object and set the page size to letter
        # c = canvas.Canvas("example.pdf", pagesize=letter)
        text = None
        # Create a frame object with the specified size and position
        txt_fn = f'{image_tag}.txt'
        txt_fn =os.path.join(const.META_TEXTS_PATH, txt_fn)
        
        if os.path.exists(txt_fn):
            print(f'found text!')
            with open(txt_fn, 'r') as f:
                text = f.read()
                print(f'text is: {text}')
                

        if not text:
            return

        frame = Frame(x1=page_x, y1=page_y,height=height*mm,
                                   width=width*mm, showBoundary=0,
                                   topPadding=0,
                                   leftPadding=0,
                                   rightPadding=0,
                                   bottomPadding=4,
                                   )

        # Create a sample style sheet for the paragraph object
        styles = getSampleStyleSheet()

        fiddle_style = ParagraphStyle('fiddle_style',
                        #    fontName=const.DIATYPE_FONT_NAME,
                           fontName=const.YAIR_FONT_NAME,
                           fontSize=8,
                           leading=8,
                           textColor = Color(0,0,0,1),
                           align='BOTTOM',
                           vAlign='BOTTOM',
                           alignment=TA_CENTER
                           )


        # Create a paragraph object with the desired text and formatting

        # text = "hello nice to meet you hi"

        # p = Paragraph(text, styles["Normal"])
        p = TopPadder(Paragraph(text, fiddle_style))



        # Add the paragraph to the frame
        frame.addFromList([p], self._canvas)

        # Save the PDF document
        # self._canvas.save()



        # if 'svg' in os.path.splitext(os.path.basename(image))[1]:
        #     row=self._next_row
        #     col=self._next_col

        #     new_y = (self._get_y(row)) + const.DEF_TAG_GAP
        #     new_y = (self._get_y(row)) + height 
        #     page_y = self._get_svg_page_y(y, height)
        #     page_x = self._get_svg_page_x(x, width)
        #     # print(f'is svg')
        #     drawing = svg2rlg(image)
        #     renderPDF.draw(drawing, self._canvas, x=page_x,
        #                    y=page_y)
        # else:
        #     self._canvas.drawImage(image=image,
        #                            preserveAspectRatio=preserveAspectRatio,
        #                            x=page_x,
        #                            y=page_y,
        #                            height=height*mm,
        #                            width=width*mm,
        #                            anchor=const.DEF_CS_ANCHOR)



    def _draw_image(self, image, preserveAspectRatio, x, y, height, width):
        # if 'svg' in os.path.splitext(os.path.basename(image))[1]:
        #     self.draw_svg()
        #     return

        page_x = self._get_page_x(x, width)
        page_y = self._get_page_y(y, height)

        # print(f'image: {image}')

        if 'svg' in os.path.splitext(os.path.basename(image))[1]:
            row=self._next_row
            col=self._next_col

            new_y = (self._get_y(row)) + const.DEF_TAG_GAP
            new_y = (self._get_y(row)) + height 
            page_y = self._get_svg_page_y(y, height)
            page_x = self._get_svg_page_x(x, width)
            # print(f'is svg')
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
        # return self._get_page_y(y, height)
        return (self._page_h - y)*mm

    def _get_svg_page_x(self, x, width):
        return self._get_page_x(x, width)
        widths_offset = const.SVG_OUTPUT_W - width
        return (self._page_w - x - width - 0.2) * mm

    def _get_im_height(self, image_cell):

        height = (image_cell.get_n_rows() * self._cell_h) - self.tag_height_mm
        return height
    

    def _get_im_width(self, image_cell):

        width=image_cell.get_n_cols() * self._cell_w
        return width

    def save(self):
        self._canvas.save()
