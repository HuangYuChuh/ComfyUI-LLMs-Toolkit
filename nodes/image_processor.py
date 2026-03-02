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
                "image_2": ("IMAGE", {"default": None}),
                "image_3": ("IMAGE", {"default": None}),
                "image_4": ("IMAGE", {"default": None}),
                "format": (["PNG", "JPEG", "WebP", "GIF", "BMP", "TIFF"], {"default": "PNG"}),
                "quality": (["High", "Medium", "Low"], {"default": "High"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_image",)
    FUNCTION = "preprocess"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Image"

    def _tensor_to_pil(self, tensor: torch.Tensor) -> Image.Image:
        """Convert a single [H, W, C] tensor to PIL Image."""
        numpy_image = tensor.cpu().numpy()
        if len(numpy_image.shape) == 3 and numpy_image.shape[2] == 1:
            numpy_image = numpy_image.squeeze(-1)
        numpy_image = (numpy_image * 255).astype('uint8')
        return Image.fromarray(numpy_image)

    def preprocess(self, image: Optional[Union[str, Image.Image, torch.Tensor]] = None,
                   image_2: Optional[Union[str, Image.Image, torch.Tensor]] = None,
                   image_3: Optional[Union[str, Image.Image, torch.Tensor]] = None,
                   image_4: Optional[Union[str, Image.Image, torch.Tensor]] = None,
                   format: str = "PNG", quality: str = "High"):
        quality_map = {"High": 95, "Medium": 75, "Low": 50}
        quality_str = quality
        quality_val = quality_map.get(quality_str, 95)
        
        images_to_process = [img for img in [image, image_2, image_3, image_4] if img is not None]
        
        if not images_to_process:
            raise ValueError("At least one image input must be provided.")

        image_urls = []

        for img in images_to_process:
            if isinstance(img, torch.Tensor):
                if len(img.shape) == 4:
                    for i in range(img.shape[0]):
                        pil_image = self._tensor_to_pil(img[i])
                        url = self._process_single_image(pil_image, format, quality_str, quality_val)
                        image_urls.append(url)
                else:
                    pil_image = self._tensor_to_pil(img)
                    url = self._process_single_image(pil_image, format, quality_str, quality_val)
                    image_urls.append(url)

            elif isinstance(img, Image.Image):
                # Single PIL image
                url = self._process_single_image(img, format, quality_str, quality_val)
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
        save_kwargs = {"format": format}
        if format in ["JPEG", "WebP"]:
            save_kwargs["quality"] = quality_val
        
        image.save(buffered, **save_kwargs)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        image_url = f"data:image/{format.lower()};base64,{img_str}"
        
        size_kb = buffered.tell() / 1024
        print(f"[LLMs_Toolkit] encoded={size_kb:.1f}KB {format} ({image.width}x{image.height})")
        
        return image_url


# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {"ImagePreprocessor": ImagePreprocessor}
NODE_DISPLAY_NAME_MAPPINGS = {"ImagePreprocessor": "Image Preprocessor"}
