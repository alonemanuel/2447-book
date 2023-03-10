from utilities.cell_sizer import CellSizer
import os

SINGLE_CELLED = CellSizer(1, 1)
MEDIUM_CELLED = CellSizer(4, 3)
SINGLE_PAGE_CELLED = CellSizer(-1, -1)
DOUBLE_PAGE_CELLED = CellSizer(-1, -1)


INPUTS_PATH = os.path.join('inputs')
OUTPUTS_PATH = os.path.join('outputs')
FIVE_SAMPLES_PATH = os.path.join(INPUTS_PATH, '005_samples')
FIFTEEN_SAMPLES_PATH = os.path.join(INPUTS_PATH, '015_samples')
FIFTY_SAMPLES_PATH = os.path.join(INPUTS_PATH, '050_samples')
HUNDRED_SAMPLES_PATH = os.path.join(INPUTS_PATH, '100_samples')

PEOPLE_FEEDBACK_SAMPLES = os.path.join('..', 'assets', 'people_sample')
BIGER_PEOPLE_FEEDBACK_SAMPLES = os.path.join('..', 'assets', 'bigger_people_samples')
BIGER_EDGES_PEOPLE_FEEDBACK_SAMPLES = os.path.join('..', 'assets', 'bigger_edges_people_samples')

ASSETS_TYPE = 'assets'
CONTACTSHEETS_TYPE = 'contactsheets'

ORIG_PART_NAME = 'orig'
EDGED_PART_NAME = 'edged'
GIF_PART_NAME = 'gif'

DEF_SIGMA = 0.33  # Lower sigma - less details
HIGH_SIGMA = 0.66


ORIG_CS_N_ROWS = 9
ORIG_CS_N_COLS = 6

EDGED_CS_N_ROWS = 9
EDGED_CS_N_COLS = 6

PAGE_W = 152
PAGE_H = 252
PAGE_GAP_MM = 2
# PAGE_ROW_GAP = 2
# PAGE_ROW_GAP = 2

DIATYPE_FONT_NAME = 'ABCDiatype'
DIATYPE_FONT_PATH = os.path.join(    'assets', 'fonts', 'ABCDiatype-Regular-Trial.ttf')
EDITORIAL_FONT_NAME = 'PPEditorial'
EDITORIAL_FONT_PATH = os.path.join(
    'assets', 'fonts', 'PPEditorialNew-Regular.ttf')
    
YAIR_FONT_NAME = 'Yair'
YAIR_FONT_PATH = os.path.join(
    'assets', 'fonts', 'NarkissYairMono-Regular-TRIAL.ttf')
DEF_FONT_TAG_SIZE = 7.5
DEF_TAG_GAP = 2.8
# DEF_TAG_GAP = 2.5
DEF_TAG_NUDGE = 3.2


DEF_CS_ANCHOR = 's'

MED_SIZE_SN_LIST = [
    '0261',
    '0322',
    '0356',
    '0420',
    '0666',
    '0741',
    '0896',
    '1018',
    '1065',
    '1188',
    '1190',
    '1360',
    '1566',
    '1655',
    '1677',
    '1801',
    '2060',
    '2172'
]

FULL_SIZE_SN_LIST = [
    '1501',
    '1031',
    '0230',


]

DOUBLE_SIZE_SN_LIST = [
    '1311',
    '1426',
    '1383'

]

ASSETS_PATH = os.path.join('..', 'assets')

ALL_STILLS_PATH = os.path.join(ASSETS_PATH, 'orig_copy', 'stills')
RANDOM_SAMPLE_DIR = os.path.join(OUTPUTS_PATH, 'random_sample')


MEDIUM_STILLS_PATH = os.path.join(ASSETS_PATH, 'medium_size_stills')
SINGLE_PAGE_STILLS_PATH = os.path.join(ASSETS_PATH, 'single_page_stills')
DOUBLE_PAGE_STILLS_PATH = os.path.join(ASSETS_PATH, 'double_page_stills')

GIFS_INPUT_DIR = os.path.join(INPUTS_PATH, 'gif_samples')
GIFS_OUTPUT_DIR = os.path.join(OUTPUTS_PATH, 'gif_outputs')
GIFS_BATCHED_INPUT_DIR = os.path.join(INPUTS_PATH, 'gif_batch_samples')
GIFS_BATCHED_INPUT_DIR = os.path.join(INPUTS_PATH, 'gif_batch_samples')
N_GIFS_TO_SAVE = 3
DEF_GIF_COL_GAP = 0
DEF_GIF_ROW_GAP = 3
GIF_CS_N_COLS = 6
GIF_CS_N_ROWS = 10


META_PART_NAME = 'metadata'
META_CS_N_ROWS = 10
META_CS_N_COLS = 7
DEF_META_COL_GAP = 3
DEF_META_ROW_GAP = 3
DEF_PALETTE_SIZE = 4

DEF_COLOR_UNIQUE_THRESH = 20

SVG_OUTPUT_W = 19.142857142857142
SVG_OUTPUT_H = 22


NN_MODELS_DIR = os.path.join('nn_models')
DEPLOY_FN = os.path.join(NN_MODELS_DIR, 'deploy.prototxt')
CAFFE_MODEL = os.path.join(NN_MODELS_DIR, 'res10_300x300_ssd_iter_140000_fp16.caffemodel')

META_TEXTS_PATH = os.path.join(OUTPUTS_PATH, META_PART_NAME, 'texts')