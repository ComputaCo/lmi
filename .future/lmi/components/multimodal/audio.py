import numpy as np
from pydub import AudioSegment

from lmi.components.core.media.description import Description


class Audio(Description.variant(AudioSegment | np.array)):
    autoplay: bool = False
    loop: bool = False
    # TOOD: implement autoplay and loop on video as well
    # Add Tools to interacting with video/audio
    # Make an AbstractMedia Description.variant class

    def loader(path):
        if path.suffix == ".wav":
            return AudioSegment.from_wav(path)
        elif path.suffix == ".mp3":
            return AudioSegment.from_mp3(path)
        elif path.suffix == ".ogg":
            return AudioSegment.from_ogg(path)
        elif path.suffix == ".flac":
            return AudioSegment.from_flac(path)
        elif path.suffix == ".aiff":
            return AudioSegment.from_file(path, format="aac")
        elif path.suffix == ".mp4":
            return AudioSegment.from_file(path, format="mp4")
        elif path.suffix == ".m4a":
            return AudioSegment.from_file(path, format="m4a")
        elif path.suffix == ".wma":
            return AudioSegment.from_file(path, format="wma")
        else:
            raise ValueError(f"Unsupported audio format: {path.suffix}")
