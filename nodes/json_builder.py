import json
from typing import Tuple


class JSONBuilder:
    """
    Build JSON object from key-value pairs.
    
    Enter key names in the multiline text box (one per line).
    Connect values to the value_1 ~ value_10 inputs.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "keys": ("STRING", {
                    "default": "key1\nkey2",
                    "multiline": True,
                    "dynamicPrompts": False,
                }),
            },
            "optional": {
                "value_1": ("STRING", {"default": "", "forceInput": True}),
                "value_2": ("STRING", {"default": "", "forceInput": True}),
                "value_3": ("STRING", {"default": "", "forceInput": True}),
                "value_4": ("STRING", {"default": "", "forceInput": True}),
                "value_5": ("STRING", {"default": "", "forceInput": True}),
                "value_6": ("STRING", {"default": "", "forceInput": True}),
                "value_7": ("STRING", {"default": "", "forceInput": True}),
                "value_8": ("STRING", {"default": "", "forceInput": True}),
                "value_9": ("STRING", {"default": "", "forceInput": True}),
                "value_10": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "build"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/JSON"
    DESCRIPTION = """
Build JSON from key-value pairs.

**Usage:**
1. Enter key names in the text box (one per line)
2. Connect values to value_1, value_2, etc.
3. Line 1 → value_1, Line 2 → value_2, ...

Supports up to 10 key-value pairs.
"""

    def build(self, keys: str, **kwargs) -> Tuple[str]:
        """Build JSON from key-value pairs."""
        result = {}
        
        # Parse keys from multiline text
        key_list = [k.strip() for k in keys.strip().split('\n') if k.strip()]
        
        # Match keys with values
        for i, key in enumerate(key_list[:10], start=1):
            value = kwargs.get(f"value_{i}", "")
            
            if key:
                # Try to parse value as JSON, otherwise use as string
                try:
                    parsed_value = json.loads(value)
                    result[key] = parsed_value
                except (json.JSONDecodeError, TypeError):
                    result[key] = value if value else ""
        
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        print(f"# [🚦 LLMs_Toolkit] built JSON with {len(result)} keys")
        return (json_str,)


# Register the node
NODE_CLASS_MAPPINGS = {"JSONBuilder": JSONBuilder}
NODE_DISPLAY_NAME_MAPPINGS = {"JSONBuilder": "JSON Builder"}
