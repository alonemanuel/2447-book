from utilities.book_part import BookPart
import utilities.constants as const
from utilities.preprocessors import orig_preprocessor, edged_preprocessor
import random
import shutil
import os
import utilities.utils


def main():

    # create_all_contactsheets()
    # create_random_sample(files_dir_path=const.ALL_STILLS_PATH, dest_folder=const.RANDOM_SAMPLE_DIR,n_samples=3)
    utilities.utils.save_gifs_to_frames()

def create_all_contactsheets():
    print(f'Creating all contactsheets...')
    orig_part = BookPart(raw_input_dir=const.ALL_STILLS_PATH,
                         part_name=const.ORIG_PART_NAME,
                         preprocessor_class=orig_preprocessor.OrigPreprocessor,
                         cs_n_rows=const.ORIG_CS_N_ROWS,
                         cs_n_cols=const.ORIG_CS_N_COLS
                         )
    edged_part = BookPart(raw_input_dir=const.HUNDRED_SAMPLES_PATH,
                          part_name=const.EDGED_PART_NAME,
                          preprocessor_class=edged_preprocessor.EdgedPreprocessor,
                          cs_n_rows=const.EDGED_CS_N_ROWS,
                          cs_n_cols=const.EDGED_CS_N_COLS
                          )

    orig_part.preprocess_inputs()
    # edged_part.preprocess_inputs()
    orig_part.create_contactsheets()
    # edged_part.create_contactsheets()
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
