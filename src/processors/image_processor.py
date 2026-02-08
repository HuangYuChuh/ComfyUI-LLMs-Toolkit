import base64
import io
from PIL import Image
from typing import Optional, Union
import torch

class ImagePreprocessor:
    """
    Custom node for preprocessing images before passing them to LLMs.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"default": None}),
            },
            "optional": {
                "format": (["PNG", "JPEG", "WebP", "GIF", "BMP", "TIFF"], {"default": "PNG"}),
                "quality": (["High", "Medium", "Low"], {"default": "High"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_image",)
    FUNCTION = "preprocess"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Image"

    def preprocess(self, image: Optional[Union[str, Image.Image]], format: str = "PNG", quality: str = "High"):
        quality_map = {"High": 95, "Medium": 75, "Low": 50}
        quality_str = quality  # Ensure quality is treated as a string
        quality_val = quality_map.get(quality_str, 95)  # Default to High if invalid value
        print(f"Selected quality: {quality_val}")  # Debugging line

        if image is None:
            raise ValueError("Image input cannot be None")

        # Convert image to PIL object if it's a tensor
        if isinstance(image, torch.Tensor):
            numpy_image = image.squeeze(0).cpu().numpy()  # [H, W, C]
            if len(numpy_image.shape) == 3 and numpy_image.shape[2] == 1:  # Grayscale image
                numpy_image = numpy_image.squeeze(-1)
            numpy_image = (numpy_image * 255).astype('uint8')
            image = Image.fromarray(numpy_image)

        # Ensure the image is a PIL object
        elif not isinstance(image, Image.Image):
            raise ValueError("Unsupported image type. Expected torch.Tensor or PIL.Image.")

        # Resize image based on quality
        size_map = {"High": 1024, "Medium": 768, "Low": 512}
        max_size = size_map.get(quality_str, 1024)
        print(f"Resizing image to max dimension: {max_size}")
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        # Convert PIL image to base64 string
        buffered = io.BytesIO()
        image.save(buffered, format=format, quality=quality_val)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        image_url = f"data:image/{format.lower()};base64,{img_str}"
        print(f"Image size with quality {quality}: {buffered.tell()} bytes")
        print(f"Generated image URL: {image_url[:50]}...")  # 打印生成的图像 URL 前 50 个字符

        return (image_url,)


# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {"ImagePreprocessor": ImagePreprocessor}
NODE_DISPLAY_NAME_MAPPINGS = {"ImagePreprocessor": "Image Preprocessor"}
