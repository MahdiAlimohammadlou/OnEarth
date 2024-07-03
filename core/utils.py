from PIL import Image
from django.db import models

def get_current_url(request):
    return request.scheme + "://" + request.get_host()

def get_full_url(obj, field_name, base_url):
    field = getattr(obj, field_name)
    if field != "":
        return base_url + field.url
    else:
        return ""

class ImageCompressionClass:
    @staticmethod
    def reduce_image_size(image_path, output_size=(800, 600)):
        """
        Resize an image to the specified size and replace the original image with the resized version.
        
        :param image_path: Path to the original image.
        :param output_size: Tuple specifying the new size (width, height).
        """
        with Image.open(image_path) as img:
            original_size = img.size
            if original_size[0] < output_size[0] or original_size[1] < output_size[1]:
                return
            img = img.resize(output_size, Image.Resampling.LANCZOS)
            img.save(image_path)

def compress_model_images(instance) -> None:
    """
    Compress images for a given model instance.
    """
    for field in instance._meta.get_fields():
        if isinstance(field, models.ImageField):
            image_field = getattr(instance, field.name)
            if image_field and image_field.path:
                try:
                    ImageCompressionClass.reduce_image_size(image_field.path)
                except FileNotFoundError:
                    print(f"File {image_field.path} not found. Skipping resize.")