import numpy as np
from colorthief import ColorThief, MMCQ, PQueue, CMap
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie1976
import colorspacious


class MyColorThief(ColorThief):
    def __init__(self, image):
        self.image = image

    def color_difference(self, color1, color2):
        color1_lab = colorspacious.cspace_convert(
            [color1[0]/255, color1[1]/255, color1[2]/255], "sRGB255", "CIELAB")
        color2_lab = colorspacious.cspace_convert([color2[0]/255, color2[1]/255, color2[2]/255], "sRGB255", "CIELAB"
                                                  )
        return sum((color1_lab - color2_lab)**2)**0.5

    def filter_similar_colors(self, colors, threshold=20):
        filtered_colors = []
        for color1 in colors:
            add_color = True
            for color2 in filtered_colors:
                if self.color_difference(color1, color2) < threshold:
                    add_color = False
                    break
            if add_color:
                filtered_colors.append(color1)
        return filtered_colors

    import colorspacious

    def unique_colors(self, colors, threshold=10.0, color_space='sRGB255'):
        unique_colors = []
        for color in colors:
            # color = np.array(color)
            add = True
            for unique_color in unique_colors:
                if colorspacious.deltaE(color, unique_color, color_space) < threshold:
                    add = False
                    break
            if add:
                unique_colors.append(color)
        return unique_colors


    def old_get_palette(self, color_count=10, quality=10, frequency_threshold=None):
        """Build a color palette.  We are using the median cut algorithm to
        cluster similar colors.

        :param color_count: the size of the palette, max number of colors
        :param quality: quality settings, 1 is the highest quality, the bigger
                        the number, the faster the palette generation, but the
                        greater the likelihood that colors will be missed.
        :param frequency_threshold: the minimum frequency required for a color to be included in the palette
        :return list: a list of tuple in the form (r, g, b)
        """
        image = self.image.convert('RGBA')
        width, height = image.size
        pixels = image.getdata()
        pixel_count = width * height
        valid_pixels = []
        for i in range(0, pixel_count, quality):
            r, g, b, a = pixels[i]
            # If pixel is mostly opaque and not white
            if a >= 125:
                if not (r > 250 and g > 250 and b > 250):
                    valid_pixels.append((r, g, b))

        if frequency_threshold:
            color_count = min(color_count, len(valid_pixels))
            color_frequency = {}
            for color in valid_pixels:
                if color in color_frequency:
                    color_frequency[color] += 1
                else:
                    color_frequency[color] = 1

            valid_pixels = [color for color, frequency in color_frequency.items() if frequency/pixel_count >= frequency_threshold]
            valid_pixels = sorted(valid_pixels, key=lambda x: color_frequency[x], reverse=True)[:color_count]

        # Send array to quantize function which clusters values
        # using median cut algorithm
        cmap = MMCQ.quantize(valid_pixels, color_count)
        return cmap.palette


    def get_palette(self, color_count=10, quality=10):
        image = self.image.convert('RGBA')
        width, height = image.size
        pixels = image.getdata()
        pixel_count = width * height
        valid_pixels = []
        for i in range(0, pixel_count, quality):
            r, g, b, a = pixels[i]
            # If pixel is mostly opaque and not white
            if a >= 125:
                if not (r > 250 and g > 250 and b > 250):
                    valid_pixels.append((r, g, b))

        # Send array to quantize function which clusters values
        # using median cut algorithm
        cmap = MyMMCQ.quantize(valid_pixels, color_count)
        # colors = [(255, 0, 0), (255, 51, 51), (255, 102, 102), (0, 0, 255), (51, 51, 255), (102, 102, 255)]
        return cmap.palette
# filtered_colors = filter_similar_colors(colors)
# print(filtered_colors)


class MyMMCQ(MMCQ):

    @staticmethod
    def quantize(pixels, max_color):
        """Quantize.

        :param pixels: a list of pixel in the form (r, g, b)
        :param max_color: max number of colors
        """
        if not pixels:
            raise Exception('Empty pixels when quantize.')
        if max_color < 2 or max_color > 256:
            raise Exception('Wrong number of max colors when quantize.')

        histo = MMCQ.get_histo(pixels)

        # check that we aren't below maxcolors already
        if len(histo) <= max_color:
            # generate the new colors from the histo and return
            pass

        # get the beginning vbox from the colors
        vbox = MMCQ.vbox_from_pixels(pixels, histo)
        n_pixels_thresh = 0.2 * len(pixels) 
        pq = MyPQueue(lambda x: x.count, n_pixels_thresh)
        pq.push(vbox)

        # inner function to do the iteration
        def iter_(lh, target):
            n_color = 1
            n_iter = 0
            while n_iter < MMCQ.MAX_ITERATION:
                vbox = lh.pop()
                if not vbox.count:  # just put it back
                    lh.push(vbox)
                    n_iter += 1
                    continue
                # do the cut
                vbox1, vbox2 = MMCQ.median_cut_apply(histo, vbox)
                if not vbox1:
                    raise Exception("vbox1 not defined; shouldn't happen!")
                lh.push(vbox1)
                if vbox2:  # vbox2 can be null
                    lh.push(vbox2)
                    n_color += 1
                if n_color >= target:
                    return
                if n_iter > MMCQ.MAX_ITERATION:
                    return
                n_iter += 1

        # first set of colors, sorted by population
        iter_(pq, MMCQ.FRACT_BY_POPULATIONS * max_color)

        # Re-sort by the product of pixel occupancy times the size in
        # color space.
        pq2 = PQueue(lambda x: x.count * x.volume)
        while pq.size():
            pq2.push(pq.pop())

        # next set - generate the median cuts using the (npix * vol) sorting.
        iter_(pq2, max_color - pq2.size())

        # calculate the actual colors
        cmap = CMap()
        while pq2.size():
            cmap.push(pq2.pop())
        return cmap


class MyPQueue(PQueue):
    def __init__(self, sort_key, n_pixels):
        self.n_pixels_thresh = n_pixels
        super().__init__(sort_key)

    def push(self, o):
        # if o.count > self.n_pixels_thresh:
        self.contents.append(o)
        self._sorted = False
