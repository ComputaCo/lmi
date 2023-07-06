from PIL.Image import Image

from gptos.lmi.components.description import Description


Image = Description.variant("Image", Image, loader=lambda path: Image.open(path))
