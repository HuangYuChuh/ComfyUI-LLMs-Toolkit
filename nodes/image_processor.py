import base64
import json
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
        quality_str = quality
        quality_val = quality_map.get(quality_str, 95)
        
        if image is None:
            raise ValueError("Image input cannot be None")

        # Result list
        image_urls = []

        # Handle Tensor Batch [B, H, W, C]
        if isinstance(image, torch.Tensor):
            # Check if it's a batch (4D) or single (3D)
            if len(image.shape) == 4:
                # Batch processing
                for i in range(image.shape[0]):
                    # Extract single image [H, W, C]
                    single_image = image[i]
                    numpy_image = single_image.cpu().numpy()
                    if len(numpy_image.shape) == 3 and numpy_image.shape[2] == 1:  # Grayscale
                         numpy_image = numpy_image.squeeze(-1)
                    numpy_image = (numpy_image * 255).astype('uint8')
                    pil_image = Image.fromarray(numpy_image)
                    
                    url = self._process_single_image(pil_image, format, quality_str, quality_val)
                    image_urls.append(url)
            else:
                # Single tensor image (e.g. from some other nodes?)
                numpy_image = image.cpu().numpy()
                if len(numpy_image.shape) == 3 and numpy_image.shape[2] == 1:
                     numpy_image = numpy_image.squeeze(-1)
                numpy_image = (numpy_image * 255).astype('uint8')
                pil_image = Image.fromarray(numpy_image)
                
                url = self._process_single_image(pil_image, format, quality_str, quality_val)
                image_urls.append(url)

        elif isinstance(image, Image.Image):
            # Single PIL image
            url = self._process_single_image(image, format, quality_str, quality_val)
            image_urls.append(url)
        
        else:
            raise ValueError("Unsupported image type. Expected torch.Tensor or PIL.Image.")

        # If only one image, return as string for backward compatibility? 
        # Plan says: "ImagePreprocessor output will change from str to List[str]"
        # To be safe for ComfyUI string passing, let's return a list
        # We use JSON serialization to avoid ComfyUI auto-batching the list
        return (json.dumps(image_urls),)

    def _process_single_image(self, image: Image.Image, format: str, quality_str: str, quality_val: int) -> str:
        # Resize image
        size_map = {"High": 1024, "Medium": 768, "Low": 512}
        max_size = size_map.get(quality_str, 1024)
        
        w, h = image.size
        # Only resize if larger than max_size
        if max(w, h) > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            # print(f"[LLMs_Toolkit] resize={max_size}px")

        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format=format, quality=quality_val)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        image_url = f"data:image/{format.lower()};base64,{img_str}"
        
        size_kb = buffered.tell() / 1024
        print(f"[LLMs_Toolkit] encoded={size_kb:.1f}KB {format} ({image.width}x{image.height})")
        
        return image_url


# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {"ImagePreprocessor": ImagePreprocessor}
NODE_DISPLAY_NAME_MAPPINGS = {"ImagePreprocessor": "Image Preprocessor"}
