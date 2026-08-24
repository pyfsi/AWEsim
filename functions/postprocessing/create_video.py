import imageio.v2 as imageio
import numpy as np
from pathlib import Path


def create_video(
    input_folder,
    output_file,
    prefix="Pressure_",
    start=5,
    stop=405,
    step=5,
    fps=20,
):
    """
    Create an MP4 video from a sequence of PNG images.

    Parameters
    ----------
    input_folder : str or Path
        Folder containing the PNG images.
    output_file : str or Path
        Path of the output MP4 file.
    prefix : str, optional
        Prefix of the image filenames.
    start : int, optional
        First timestep.
    stop : int, optional
        Upper limit of the timestep range (exclusive).
    step : int, optional
        Timestep increment.
    fps : int or float, optional
        Frames per second of the output video.
    """

    input_folder = Path(input_folder)
    output_file = Path(output_file)

    timesteps = np.arange(start, stop, step)

    with imageio.get_writer(
        output_file,
        fps=fps,
        format="ffmpeg",
    ) as writer:

        for timestep in timesteps:
            filename = input_folder / f"{prefix}{timestep:04d}.png"

            if not filename.exists():
                raise FileNotFoundError(f"Image not found: {filename}")

            image = imageio.imread(filename)
            writer.append_data(image)

    print(f"Video saved to: {output_file}")