from utilities.cell_sizer import CellSizer
import os

SINGLE_CELLED = CellSizer(1, 1)
MEDIUM_CELLED = CellSizer(4, 3)


INPUTS_PATH = os.path.join('..','inputs')
OUTPUTS_PATH = os.path.join('..','outputs')
FIVE_SAMPLES_PATH = os.path.join(INPUTS_PATH, '005_samples')
FIFTEEN_SAMPLES_PATH = os.path.join(INPUTS_PATH, '015_samples')
FIFTY_SAMPLES_PATH = os.path.join(INPUTS_PATH, '050_samples')

ASSETS_TYPE = 'assets'
CONTACTSHEETS_TYPE = 'contactsheets'

ORIG_PART_NAME = 'orig'
EDGED_PART_NAME = 'edged'

DEF_SIGMA = 0.33 # Lower sigma - less details
HIGH_SIGMA = 0.66


ORIG_CS_N_ROWS = 9
ORIG_CS_N_COLS = 6
EDGED_CS_N_ROWS = 11
EDGED_CS_N_COLS = 7

PAGE_W = 152
PAGE_H = 252
PAGE_GAP_MM = 2

DIATYPE_FONT_NAME = 'ABCDiatype' 
DIATYPE_FONT_PATH = os.path.join('assets','fonts','ABCDiatype-Regular-Trial.ttf')
DEF_FONT_TAG_SIZE = 7
DEF_TAG_GAP = 1