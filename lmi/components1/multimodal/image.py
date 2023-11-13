from PIL.Image import Image

from lmi.components.core.media.description import Description


Image = Description.variant("Image", Image, loader=lambda path: Image.open(path))
