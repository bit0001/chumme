import io

from kivy.core.image import Image as CoreImage

def get_image_from_blob(blob, extension):
    return CoreImage(io.BytesIO(blob), ext=extension)
