import numpy as np
from moviepy import VideoFileClip

from gptos.lmi.components.description import Description


Video = Description.variant(
    "Video", VideoFileClip | np.array, loader=lambda path: VideoFileClip(path)
)
