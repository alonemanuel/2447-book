import svgwrite
from svgwrite import mm, cm
from svgwrite.mixins import ViewBox
import os

COLORBAR_W = 5
COLORBAR_H = 10

TEXT_PADDING = 4
TEXT_START_Y = COLORBAR_H + TEXT_PADDING
TEXT_DEF_FONT_SIZE = 7
import utilities.constants as const

DEF_FONT = 'ABCDiatype'
colors = ['#202020', 'green', '#000000', 'blue', '#ffffff']

class MySVG(svgwrite.Drawing):
    # def __init__(self, filename="noname.svg", size=..., **extra):
    #     super().__init__(filename, size, **extra)

    def __init__(self, filename="noname.svg"):
        super().__init__(filename)
        self._start_offset_x = 0
        self._text_offset_y = TEXT_START_Y
        self.embed_fonts()

    def saveas(self, dir_path, pretty=False):
        full_path = os.path.join(dir_path, self.filename)
        return super().saveas(full_path, pretty)

    def embed_fonts(self):
        self.embed_font(name=const.DIATYPE_FONT_NAME,
                filename=const.DIATYPE_FONT_PATH)

    # def __init__(self, filename="noname.svg", size=..., **extra):

    #     super().__init__(filename, size, **extra)

    def add_colorbar(self, w=COLORBAR_W, h=COLORBAR_H, color='grey'):
        self.add(self.rect(insert=(self._start_offset_x*mm, 0),
                           size=(w*mm, h*mm),
                           fill=color
                           ))
        self._start_offset_x += w

    def add_colorbars(self, colors):
        for color in colors:
            self.add_colorbar(color=f'rgb{color}')

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
