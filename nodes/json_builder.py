import json
import re
from typing import Tuple, Optional


class JSONBuilder:
    """
    Build JSON object from multiple key-value inputs.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "key_1": ("STRING", {"default": ""}),
                "value_1": ("STRING", {"default": "", "forceInput": True}),
                "key_2": ("STRING", {"default": ""}),
                "value_2": ("STRING", {"default": "", "forceInput": True}),
                "key_3": ("STRING", {"default": ""}),
                "value_3": ("STRING", {"default": "", "forceInput": True}),
                "key_4": ("STRING", {"default": ""}),
                "value_4": ("STRING", {"default": "", "forceInput": True}),
                "key_5": ("STRING", {"default": ""}),
                "value_5": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "build"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/JSON"

    def build(
        self,
        key_1: str = "", value_1: str = "",
        key_2: str = "", value_2: str = "",
        key_3: str = "", value_3: str = "",
        key_4: str = "", value_4: str = "",
        key_5: str = "", value_5: str = ""
    ) -> Tuple[str]:
        """Build JSON from key-value pairs."""
        result = {}
        
        pairs = [
            (key_1, value_1), (key_2, value_2), (key_3, value_3),
            (key_4, value_4), (key_5, value_5)
        ]
        
        for key, value in pairs:
            if key and key.strip():
                # Try to parse value as JSON, otherwise use as string
                try:
                    parsed_value = json.loads(value)
                    result[key.strip()] = parsed_value
                except (json.JSONDecodeError, TypeError):
                    result[key.strip()] = value
        
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        print(f"# [🚦 LLMs_Toolkit] built JSON with {len(result)} keys")
        return (json_str,)


# Register the node
NODE_CLASS_MAPPINGS = {"JSONBuilder": JSONBuilder}
NODE_DISPLAY_NAME_MAPPINGS = {"JSONBuilder": "JSON Builder"}
