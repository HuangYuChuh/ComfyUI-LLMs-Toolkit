import json
from typing import Tuple


class JSONBuilder5:
    """Build JSON object with 5 key-value pairs."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_1": ("STRING", {"default": "key1"}),
                "key_2": ("STRING", {"default": "key2"}),
                "key_3": ("STRING", {"default": "key3"}),
                "key_4": ("STRING", {"default": "key4"}),
                "key_5": ("STRING", {"default": "key5"}),
            },
            "optional": {
                "value_1": ("STRING", {"default": "", "forceInput": True}),
                "value_2": ("STRING", {"default": "", "forceInput": True}),
                "value_3": ("STRING", {"default": "", "forceInput": True}),
                "value_4": ("STRING", {"default": "", "forceInput": True}),
                "value_5": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "build"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/JSON"
    DESCRIPTION = "Build JSON with 5 key-value pairs. Keys are editable, values are connected from upstream."

    def build(self, key_1, key_2, key_3, key_4, key_5, **kwargs) -> Tuple[str]:
        result = {}
        keys = [key_1, key_2, key_3, key_4, key_5]
        
        for i, key in enumerate(keys, start=1):
            value = kwargs.get(f"value_{i}", "")
            if key and key.strip():
                try:
                    parsed_value = json.loads(value)
                    result[key.strip()] = parsed_value
                except (json.JSONDecodeError, TypeError):
                    result[key.strip()] = value if value else ""
        
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        print(f"# [🚦 LLMs_Toolkit] built JSON with {len(result)} keys")
        return (json_str,)


class JSONBuilder10:
    """Build JSON object with 10 key-value pairs."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_1": ("STRING", {"default": "key1"}),
                "key_2": ("STRING", {"default": "key2"}),
                "key_3": ("STRING", {"default": "key3"}),
                "key_4": ("STRING", {"default": "key4"}),
                "key_5": ("STRING", {"default": "key5"}),
                "key_6": ("STRING", {"default": "key6"}),
                "key_7": ("STRING", {"default": "key7"}),
                "key_8": ("STRING", {"default": "key8"}),
                "key_9": ("STRING", {"default": "key9"}),
                "key_10": ("STRING", {"default": "key10"}),
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
    DESCRIPTION = "Build JSON with 10 key-value pairs. Keys are editable, values are connected from upstream."

    def build(self, key_1, key_2, key_3, key_4, key_5, 
              key_6, key_7, key_8, key_9, key_10, **kwargs) -> Tuple[str]:
        result = {}
        keys = [key_1, key_2, key_3, key_4, key_5,
                key_6, key_7, key_8, key_9, key_10]
        
        for i, key in enumerate(keys, start=1):
            value = kwargs.get(f"value_{i}", "")
            if key and key.strip():
                try:
                    parsed_value = json.loads(value)
                    result[key.strip()] = parsed_value
                except (json.JSONDecodeError, TypeError):
                    result[key.strip()] = value if value else ""
        
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        print(f"# [🚦 LLMs_Toolkit] built JSON with {len(result)} keys")
        return (json_str,)


# Register nodes
NODE_CLASS_MAPPINGS = {
    "JSONBuildCompact": JSONBuilder5,
    "JSONBuildExtended": JSONBuilder10,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JSONBuildCompact": "JSON Build ×5",
    "JSONBuildExtended": "JSON Build ×10",
}
