from utilities.cell_sizer import CellSizer
import os

SINGLE_CELLED = CellSizer(1, 1)
MEDIUM_CELLED = CellSizer(4, 3)


INPUTS_PATH = os.path.join('inputs')
OUTPUTS_PATH = os.path.join('outputs')
FIVE_SAMPLES_PATH = os.path.join(INPUTS_PATH, '005_samples')

ASSETS_TYPE = 'assets'
CONTACTSHEETS_TYPE = 'contactsheets'

ORIG_PART_NAME = 'orig'
EDGED_PART_NAME = 'edged'

DEF_SIGMA = 0.33