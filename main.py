from utilities.book_part import BookPart
import utilities.constants as const
from utilities.preprocessors import preprocessor, meta_preprocessor, orig_preprocessor, edged_preprocessor
import random
import shutil
import os
import utilities.utils


def main():

    # create_all_contactsheets()
    # create_random_sample(files_dir_path=const.ALL_STILLS_PATH, dest_folder=const.RANDOM_SAMPLE_DIR,n_samples=3)
    # utilities.utils.save_gifs_to_frames()
    # create_gif_contactsheets()
    create_meta_contactsheets()
    # create_all_contactsheets()
    # create_orig_contactsheets()
    # create_edged_contactsheets()
    # create_edged_gifs()
    # resize_edges(2.5)
    # create_edges_samples()


def create_orig_contactsheets():
    orig_part = BookPart(raw_input_dir=const.FIFTEEN_SAMPLES_PATH,
                         part_name=const.ORIG_PART_NAME,
                         preprocessor_class=orig_preprocessor.OrigPreprocessor,
                         cs_n_rows=const.ORIG_CS_N_ROWS,
                         cs_n_cols= const.ORIG_CS_N_COLS,
                         row_gap=const.PAGE_GAP_MM,
                         col_gap=const.PAGE_GAP_MM,
                         is_batched=False,
                         image_limit=5
                         )
    orig_part.create_contactsheets(image_limit=3000)

def create_meta_contactsheets():
    meta_part = BookPart(raw_input_dir=const.ALL_STILLS_PATH,
                         part_name=const.META_PART_NAME,
                         preprocessor_class=meta_preprocessor.MetaPreprocessor,
                         cs_n_rows=const.META_CS_N_ROWS,
                         cs_n_cols=const.META_CS_N_COLS,
                         row_gap=const.DEF_META_ROW_GAP,
                         col_gap=const.DEF_META_COL_GAP,
                         is_batched=False
                         )
    meta_part.preprocess_inputs()
    meta_part.create_contactsheets(image_limit=3000)


def create_gif_contactsheets():
    gifs_part = BookPart(raw_input_dir=const.GIFS_BATCHED_INPUT_DIR,
                         part_name=const.GIF_PART_NAME,
                         preprocessor_class=orig_preprocessor.OrigPreprocessor,
                         cs_n_rows=const.GIF_CS_N_ROWS,
                         cs_n_cols=const.GIF_CS_N_COLS,
                         row_gap=const.DEF_GIF_ROW_GAP,
                         col_gap=const.DEF_GIF_COL_GAP,
                         is_batched=True, 
                         )


    gifs_part.create_contactsheets(image_limit=3000, row_start=4,col_start=3)

def create_edged_gifs():
    gifs_part = BookPart(raw_input_dir=const.GIFS_BATCHED_INPUT_DIR,
                         part_name=const.GIF_PART_NAME,
                         preprocessor_class=edged_preprocessor.EdgedPreprocessor,
                         cs_n_rows=const.GIF_CS_N_ROWS,
                         cs_n_cols=const.GIF_CS_N_COLS,
                         row_gap=const.DEF_GIF_ROW_GAP,
                         col_gap=const.DEF_GIF_COL_GAP,
                         is_batched=True, 
                         )

    # gifs_part.preprocess_inputs()


    gifs_part.create_contactsheets(image_limit=2, row_start=4,col_start=3)

def create_edges_samples():
    print(f'creating edges...')
    input_dir = const.BIGER_PEOPLE_FEEDBACK_SAMPLES
    output_dir = const.BIGER_EDGES_PEOPLE_FEEDBACK_SAMPLES
    edger = edged_preprocessor.EdgedPreprocessor(input_dir=input_dir, output_dir=output_dir)
    for im in os.listdir(input_dir):
        edger.preprocess(im, big_lines=True)


def resize_edges(resize_factor =3):
    print(f'resizing edges...')
    input_dir = const.PEOPLE_FEEDBACK_SAMPLES 
    output_dir = const.BIGER_PEOPLE_FEEDBACK_SAMPLES
    from PIL import Image


    INPUT_DIR = input_dir
    OUTPUT_DIR = output_dir

    # Loop through all files in the input directory
    for filename in os.listdir(INPUT_DIR):
        # Open the image
        img = Image.open(os.path.join(INPUT_DIR, filename))

        # Get the current size of the image
        width, height = img.size

        # Calculate the new size
        new_width = int(width * resize_factor)
        new_height = int(height * resize_factor)

        # Resize the image
        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        # Save the resized image to the output directory
        img.save(os.path.join(OUTPUT_DIR, filename))



def create_edged_contactsheets():
    print(f'Creating all contactsheets...')
    # orig_part = BookPart(raw_input_dir=const.ALL_STILLS_PATH,
    #                      part_name=const.ORIG_PART_NAME,
    #                      preprocessor_class=orig_preprocessor.OrigPreprocessor,
    #                      cs_n_rows=const.ORIG_CS_N_ROWS,
    #                      cs_n_cols=const.ORIG_CS_N_COLS
    #                      )
    edged_part = BookPart(raw_input_dir=const.ALL_STILLS_PATH,
                          part_name=const.EDGED_PART_NAME,
                          preprocessor_class=edged_preprocessor.EdgedPreprocessor,
                          cs_n_rows=const.EDGED_CS_N_ROWS,
                          cs_n_cols=const.EDGED_CS_N_COLS,
                          row_gap=const.DEF_GIF_ROW_GAP,
                          col_gap=const.DEF_GIF_COL_GAP,
                          is_batched=False, image_limit=3000)

    # orig_part.preprocess_inputs()
    # edged_part.preprocess_inputs()

    edged_part.create_contactsheets(image_limit=3000)
    # edged_part.create_contactsheets(image_limit=80)
    # for book_part in [orig_part, edged_part]:
    #     print('\n\n\n')
def create_all_contactsheets():
    print(f'Creating all contactsheets...')
    # orig_part = BookPart(raw_input_dir=const.ALL_STILLS_PATH,
    #                      part_name=const.ORIG_PART_NAME,
    #                      preprocessor_class=orig_preprocessor.OrigPreprocessor,
    #                      cs_n_rows=const.ORIG_CS_N_ROWS,
    #                      cs_n_cols=const.ORIG_CS_N_COLS
    #                      )
    edged_part = BookPart(raw_input_dir=const.ALL_STILLS_PATH,
                          part_name=const.EDGED_PART_NAME,
                          preprocessor_class=edged_preprocessor.EdgedPreprocessor,
                          cs_n_rows=const.EDGED_CS_N_ROWS,
                          cs_n_cols=const.EDGED_CS_N_COLS,
                          row_gap=const.DEF_GIF_ROW_GAP,
                          col_gap=const.DEF_GIF_COL_GAP,
                          is_batched=False)

    # orig_part.preprocess_inputs()
    edged_part.preprocess_inputs()

    # orig_part.create_contactsheets()
    edged_part.create_contactsheets()
    # for book_part in [orig_part, edged_part]:
    #     print('\n\n\n')


def create_sample_folder(filenames_to_copy, dest_folder):
    for f in os.listdir(dest_folder):
        f_fullpath = os.path.join(dest_folder, f)
        os.remove(f_fullpath)
    for i, f in enumerate(filenames_to_copy):
        f_basename = os.path.basename(f)
        print(f'copying {f_basename}...')
        shutil.copy2(f, os.path.join(dest_folder, f_basename))


def create_random_sample(files_dir_path, dest_folder, n_samples):
    random_files = get_random_fns(files_dir_path, n_samples)
    create_sample_folder(random_files, dest_folder)


def get_random_fns(dir, n_fns):
    files_dir = os.listdir(dir)
    random_filenames = random.sample(files_dir, n_fns)
    random_abs_filenames = [os.path.abspath(
        os.path.join(dir, f)) for f in random_filenames]
    return random_abs_filenames


if __name__ == '__main__':
    main()
