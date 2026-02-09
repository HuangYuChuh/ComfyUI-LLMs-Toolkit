import json
from typing import Tuple


class JSONBuilder:
    """
    Build JSON object from multiple key-value inputs.
    
    Uses dynamic input count - adjust 'inputcount' and click Update 
    to add more key-value pairs.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 100, "step": 1}),
            },
            "optional": {
                "base_json": ("STRING", {"forceInput": True}),
                "key_1": ("STRING", {"default": ""}),
                "value_1": ("STRING", {"default": "", "forceInput": True}),
                "key_2": ("STRING", {"default": ""}),
                "value_2": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "build"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/JSON"
    DESCRIPTION = """
Build JSON from key-value pairs.
- Adjust **inputcount** and click Update to add more inputs.
- Connect **base_json** to chain multiple builders.
"""

    def build(self, inputcount: int, base_json: str = None, **kwargs) -> Tuple[str]:
        """Build JSON from key-value pairs."""
        
        # Start with base JSON if provided
        if base_json:
            try:
                result = json.loads(base_json)
            except json.JSONDecodeError:
                result = {}
        else:
            result = {}
        
        # Add key-value pairs
        for i in range(1, inputcount + 1):
            key = kwargs.get(f"key_{i}", "")
            value = kwargs.get(f"value_{i}", "")
            
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
