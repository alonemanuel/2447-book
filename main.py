from utilities.book_part import BookPart
import utilities.constants as const
from utilities.preprocessors import orig_preprocessor, edged_preprocessor


def main():
    create_all_contactsheets()


def create_all_contactsheets():
    print(f'Creating all contactsheets...')
    orig_part = BookPart(raw_input_dir=const.FIVE_SAMPLES_PATH,
                         part_name=const.ORIG_PART_NAME,
                         preprocessor_class=orig_preprocessor.OrigPreprocessor,
                         cs_n_rows=const.ORIG_CS_N_ROWS,
                         cs_n_cols=const.ORIG_CS_N_COLS
                         )
    edged_part = BookPart(raw_input_dir=const.FIVE_SAMPLES_PATH,
                          part_name=const.EDGED_PART_NAME,
                          preprocessor_class=edged_preprocessor.EdgedPreprocessor,
                          cs_n_rows=const.EDGED_CS_N_ROWS,
                          cs_n_cols=const.EDGED_CS_N_COLS
                          )

    for book_part in [orig_part, edged_part]:
        print('\n\n\n')
        book_part.preprocess_inputs()
        book_part.create_contactsheets()


if __name__ == '__main__':
    main()