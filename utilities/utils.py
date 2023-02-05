import imageio
import os
import utilities.constants as const


def save_gifs_to_frames():
    input_dir = const.GIFS_INPUT_DIR
    output_dir = const.GIFS_OUTPUT_DIR

    for fn in os.listdir(input_dir):
        fn_path = os.path.join(input_dir, fn)


        fn_basename_no_ext = os.path.splitext(fn)[0]
        print(f'processing gif: {fn_basename_no_ext}')
        specific_output_dir = os.path.join(output_dir, fn_basename_no_ext)
        try:
            os.makedirs(specific_output_dir)
        except FileExistsError:
            print('already exists')
            continue

        # Load the gif
        # filename = "animation.gif"
        reader = imageio.get_reader(fn_path)

        # The desired number of frames to save
        num_frames_to_save = const.N_GIFS_TO_SAVE

        # Calculate the step size
        step = max(1, len(reader) // num_frames_to_save)

        # Save every "step" frame
        for i, frame in enumerate(reader):
            if i % step == 0:
                output_fn = os.path.join(specific_output_dir, f'{fn_basename_no_ext}_{i}.png')
                imageio.imwrite(output_fn, frame)
