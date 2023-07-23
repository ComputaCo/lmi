from PIL.Image import Image

from lmi.components.media.description import Description


Image = Description.variant("Image", Image, loader=lambda path: Image.open(path))
