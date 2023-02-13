import os

class ImageCell:
    def __init__(self, image_abs_fn, cell_sizer) -> None:
        self._image_abs_fn = image_abs_fn
        self._cell_sizer = cell_sizer

    def get_image_path(self):
        return self._image_abs_fn

    def get_n_rows(self):
        return self._cell_sizer.n_rows

    def get_n_cols(self):
        return self._cell_sizer.n_cols

    def get_sizer_type(self):
        return self._cell_sizer
    
    def get_image_tag(self):
        image_basename = os.path.basename(self._image_abs_fn)
        image_tag = os.path.splitext(image_basename)[0]
        return image_tag