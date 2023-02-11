from enum import Enum
import utilities.constants as const
import svgwrite
from svgwrite import mm, cm
from svgwrite.mixins import ViewBox
import os
from functools import reduce
from collections import namedtuple
from PIL import Image
from math import ceil, floor

COLORBAR_W = 5
COLORBAR_H = 10

NEW_COLORBAR_H = 3

OUTPUT_W = const.SVG_OUTPUT_W 
OUTPUT_H = const.SVG_OUTPUT_H 

TEXT_PADDING = 4
TEXT_START_Y = COLORBAR_H + TEXT_PADDING
TEXT_DEF_FONT_SIZE = 7

DEF_FONT = 'ABCDiatype'
colors = ['#202020', 'green', '#000000', 'blue', '#ffffff']


class MetaDataType(Enum):
    COLOR = 0
    FACE = 1
    TEXT = 2


class MySVG(svgwrite.Drawing):
    # def __init__(self, filename="noname.svg", size=..., **extra):
    #     super().__init__(filename, size, **extra)

    def __init__(self, filename="noname.svg"):
        super().__init__(filename)
        self._start_offset_x = 0
        self._text_offset_y = TEXT_START_Y
        # self.w = '30mm'
        # self.h = '30mm'
        self.embed_fonts()
        

    def saveas(self, dir_path, pretty=False):
        full_path = os.path.join(dir_path, self.filename)
        return super().saveas(full_path, pretty)

    def embed_fonts(self):
        self.embed_font(name=const.DIATYPE_FONT_NAME,
                        filename=const.DIATYPE_FONT_PATH)

    # def __init__(self, filename="noname.svg", size=..., **extra):

    #     super().__init__(filename, size, **extra)

    def get_colorbars(self, colors_hex):
        colorbars = []
        start_offset = 0
        for color in colors_hex:
            colorbars.append(self.rect(insert=(0, start_offset*mm),
                                       size=(COLORBAR_W*mm, COLORBAR_H*mm),
                                       fill=f'rgb{color}'
                                       ))
            start_offset += COLORBAR_H
        return colorbars

    def get_faces_svg(self, faces_im):
        return []

    def get_texts_svg(self, texts_str):
        return []

    def add_metadata(self, colors_hex, faces_im, texts_str):
        all_lists = [colors_hex, faces_im, texts_str]
        print(f'all lists: {all_lists}')
        colorbars_svg = self.get_colorbars(colors_hex)
        faces_svg = self.get_faces_svg(faces_im)
        texts_svg = self.get_texts_svg(texts_str)
        DataList = namedtuple('DataItem', 'items type')
        all_lists = [DataList(colors_hex, MetaDataType.COLOR), DataList(
            faces_im, MetaDataType.FACE), DataList(texts_str, MetaDataType.TEXT)]
        # n_items = sum([len(l.items) for l in svgs])

        # colors_portion, faces_portion, texts_portion = [
        #     len(l) / n_items for l in all_lists]
        filtered_items = list(filter(lambda item: len(item.items), all_lists))
        print(filtered_items)
        self.add_column(filtered_items)

    def add_column(self, metadata_lists):
        item_height_ratio = 1 / len(metadata_lists)
        item_abs_height = item_height_ratio * OUTPUT_H
        print(f'column items: {metadata_lists}')
        print(f'item abs height: {item_abs_height}')
        curr_y = 0
        for i, metadata_list in enumerate(metadata_lists):
            subitem_h = item_abs_height / len(metadata_list)
            for item in metadata_list.items:
                n_items = len(metadata_list.items)
                item_h = 1 / n_items * item_abs_height
                if metadata_list.type is MetaDataType.COLOR:
                    # print(f'subitem: {item}')
                    # continue
                    self.new_add_colorbar(w=OUTPUT_W,
                                          h=NEW_COLORBAR_H,
                                          x=0,
                                          y=int(curr_y),
                                          color=f'rgb{item}')
                elif metadata_list.type is MetaDataType.FACE:
                    # print(f'face subitem: {item}')
                    self.new_add_image(w=OUTPUT_W,
                                          h=item_h,
                                          x=0,
                                          y=curr_y,
                                          image_path=item)
                elif metadata_list.type is MetaDataType.TEXT:
                    pass

                curr_y += item_h


    def new_add_colorbar(self, w, h, color, x, y):
        print(f'color: {color}')
        self.add(self.rect(insert=(x*mm, y*mm),
                           size=(w*mm, h*mm),
                           fill=color,
                           ))

    def add_colorbar(self, w=COLORBAR_W, h=COLORBAR_H, color='grey'):

        self.add(self.rect(insert=(self._start_offset_x*mm, 0),
                           size=(w*mm, h*mm),
                           fill=color
                           ))
        self._start_offset_x += w

    def add_colorbars(self, colors):
        for color in colors:
            self.add_colorbar(color=f'rgb{color}')

    def new_add_image(self, w, h, image_path,  x, y):
        w, h = int(w), int(h)
        image_abs_path = os.path.abspath(image_path)
        print(f'im w: {w}, h: {h}')
        print(f'im path: {image_path}')
        # image = svgwrite.Drawing('test0000.svg', size=('20mm', '30mm'))
        # image.add(image.image(href=image_abs_path, size=("10mm", "20mm")))
        # image.save()
        with Image.open(image_abs_path) as im:
            orig_size_w, orig_size_h = im.size
            new_size_h = floor(orig_size_h * (h / w))
            stretched_im = im.resize((int(orig_size_w), int(new_size_h)), Image.NEAREST)
        with open(image_abs_path, "wb") as f:
            stretched_im.save(f, "JPEG")
        self.add(self.image(href=image_abs_path,
                            insert=(x*mm, y*mm),
                            size=((f'{w}mm', f'{h}mm'))))


    def add_bottom_text(self, text):

        self.add(self.text(text,
                           font_size=f'{TEXT_DEF_FONT_SIZE}pt',
                           font_family=f'{DEF_FONT}',
                           #    style=f'font-size:${TEXT_DEF_FONT_SIZE}px; font-g',
                           insert=(0, self._text_offset_y*mm)))

    def tostring(self):
        str = super().tostring()
        # print(str)
        str = str.replace('width="100%"', '')
        str = str.replace('height="100%"', '')
        return str

    # def save():
    #     fileobj = io.open(self.filename, mode='w', encoding='utf-8')
    #     self.write(fileobj, pretty=pretty, indent=indent)
    #     fileobj.close()


def test_svg():

    # dwg = MySVG(size=(15*mm, 10*mm))
    dwg = MySVG()
    # dwg.add_stylesheet('style.css', title="sometext")
    g = dwg.g(class_="myclass")
    # g.add(dwg.text("lorem ipsum", insert=(10, 30)))
    # g.add(dwg.text("Reported Crimes in Sweden",
    #                insert=(10, 30),
    #                fill="rgb(255,255,0)",
    #                style="font-size:10px; font-family:Arial"))

    # dwg.add_colorbar(color='red')
    # dwg.add_colorbar(color='green')
    dwg.add_colorbars(colors=colors)
    dwg.add_bottom_text('lorem ipsum')

    # dwg.add(g)
    # r = dwg.r(class_="otherclass")
    # r.add(dwg.)

    # svg_document = svgwrite.Drawing(filename = "test-svgwrite3.svg",
    #                         size = ("1200px", "800px"))
    # #This is the line I'm stuck at
    # #svg_document.add(svg_document.style('style="font-family: Arial; font-size  : 34;'))

    # svg_document.add(svg_document.rect(insert = (900, 800), size = ("200px", "100px"), stroke_width = "1", stroke = "black", fill = "rgb(255,255,0)"))

    # svg_document.add(svg_document.text("Reported Crimes in Sweden",
    #                             insert = (410, 50),
    #                             fill = "rgb(255,255,0)",
    #                             #This is the connection to the first line that I'm stuck at
    #                             #style = 'style="font-family: Arial; font-size  : 104;'))
    # print(dwg.tostring())
    dwg.save()
