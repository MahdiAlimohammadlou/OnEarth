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
        Resize an image to fit within the specified size while maintaining the aspect ratio,
        and replace the original image with the resized version.
        
        :param image_path: Path to the original image.
        :param output_size: Tuple specifying the maximum new size (width, height).
        """
        with Image.open(image_path) as img:
            original_size = img.size
            original_width, original_height = original_size
            max_width, max_height = output_size

            # Calculate the aspect ratio
            aspect_ratio = original_width / original_height

            # Determine the new dimensions while maintaining aspect ratio
            if original_width > original_height:  # Landscape
                new_width = min(original_width, max_width)
                new_height = int(new_width / aspect_ratio)
                if new_height > max_height:
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)
            else:  # Portrait or square
                new_height = min(original_height, max_height)
                new_width = int(new_height * aspect_ratio)
                if new_width > max_width:
                    new_width = max_width
                    new_height = int(new_width / aspect_ratio)

            # Resize the image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
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