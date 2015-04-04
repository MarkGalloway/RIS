from PIL import Image as Pil_Image
from PIL import ImageOps


def resize_image(inp, outp, width=150, height=150):
    """
    Resizes an image
    """
    img = Pil_Image.open(inp)
    img.thumbnail((width, height), Pil_Image.ANTIALIAS)
    # img = ImageOps.fit(img, (width, height), Pil_Image.ANTIALIAS)
    img.save(outp, format='JPEG', quality=75)
