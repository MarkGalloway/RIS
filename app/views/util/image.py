from PIL import Image as Pil_Image
from PIL import ImageOps


def resize_image_thumb(inp, outp, width=200, height=200):
    """
    Resizes an image
    """
    img = Pil_Image.open(inp)
    img = ImageOps.fit(img, (width, height), Pil_Image.ANTIALIAS)
    img.save(outp, format='JPEG', quality=75)


def resize_image_regular(inp, outp, width=500, height=500):
    """
    Resizes an image
    """
    img = Pil_Image.open(inp)
    img.thumbnail((width, height), Pil_Image.ANTIALIAS)
    img.save(outp, format='JPEG', quality=75)
