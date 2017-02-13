from kivy.core.image import Image as CoreImage

def get_image_from_blob(blob, extension):
    return CoreImage(blob, ext=extension)
