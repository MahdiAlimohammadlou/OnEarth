from PIL import Image

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
