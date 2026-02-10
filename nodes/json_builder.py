import json
from typing import Tuple


class JSONBuilderSimple:
    """Build JSON object with 1 key-value pair."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key": ("STRING", {"default": "key"}),
            },
            "optional": {
                "value": ("STRING", {"default": "", "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "build"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/JSON"
    DESCRIPTION = "Build JSON with 1 key-value pair (Simple)."

    def build(self, key, value="") -> Tuple[str]:
        result = {}
        if key and key.strip():
            try:
                parsed_value = json.loads(value)
                result[key.strip()] = parsed_value
            except (json.JSONDecodeError, TypeError):
                result[key.strip()] = value if value else ""
        
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        print(f"# [🚦 LLMs_Toolkit] built simple JSON")
        return (json_str,)


class JSONBuilderMedium:
    """Build JSON object with 5 key-value pairs."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_1": ("STRING", {"default": ""}),
                "key_2": ("STRING", {"default": ""}),
                "key_3": ("STRING", {"default": ""}),
                "key_4": ("STRING", {"default": ""}),
                "key_5": ("STRING", {"default": ""}),
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
    DESCRIPTION = "Build JSON with 5 key-value pairs (Medium)."

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


class JSONBuilderLarge:
    """Build JSON object with 10 key-value pairs."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key_1": ("STRING", {"default": ""}),
                "key_2": ("STRING", {"default": ""}),
                "key_3": ("STRING", {"default": ""}),
                "key_4": ("STRING", {"default": ""}),
                "key_5": ("STRING", {"default": ""}),
                "key_6": ("STRING", {"default": ""}),
                "key_7": ("STRING", {"default": ""}),
                "key_8": ("STRING", {"default": ""}),
                "key_9": ("STRING", {"default": ""}),
                "key_10": ("STRING", {"default": ""}),
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
    DESCRIPTION = "Build JSON with 10 key-value pairs (Large)."

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


class JSONCombine:
    """Combine multiple JSON objects into one. Later inputs overwrite earlier ones."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "json_1": ("STRING", {"default": "", "multiline": True, "forceInput": True}),
                "json_2": ("STRING", {"default": "", "multiline": True, "forceInput": True}),
                "json_3": ("STRING", {"default": "", "multiline": True, "forceInput": True}),
                "json_4": ("STRING", {"default": "", "multiline": True, "forceInput": True}),
                "json_5": ("STRING", {"default": "", "multiline": True, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "combine"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/JSON"
    DESCRIPTION = "Combine multiple JSON objects. json_5 overrides json_4 ... overrides json_1."

    def combine(self, **kwargs):
        merged = {}
        
        # Iterate from json_1 to json_5
        for i in range(1, 6):
            key = f"json_{i}"
            json_data = kwargs.get(key, "")
            
            if not json_data or not json_data.strip():
                continue
                
            try:
                # Try parsing as JSON
                parsed = json.loads(json_data)
                
                if isinstance(parsed, dict):
                    merged.update(parsed)
                else:
                    print(f"[🚦 JSON Combine] Warning: {key} is not a JSON object (got {type(parsed)}), skipping update.")
                    
            except json.JSONDecodeError:
                print(f"[🚦 JSON Combine] Warning: {key} is not valid JSON, skipping.")
        
        json_str = json.dumps(merged, ensure_ascii=False, indent=2)
        print(f"# [🚦 LLMs_Toolkit] Combined {len(kwargs)} inputs into JSON with {len(merged)} keys")
        return (json_str,)


# Register nodes
NODE_CLASS_MAPPINGS = {
    "JSONBuilderSimple": JSONBuilderSimple,
    "JSONBuilderMedium": JSONBuilderMedium,
    "JSONBuilderLarge": JSONBuilderLarge,
    "JSONCombine": JSONCombine,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JSONBuilderSimple": "JSON Builder Simple",
    "JSONBuilderMedium": "JSON Builder Medium",
    "JSONBuilderLarge": "JSON Builder Large",
    "JSONCombine": "JSON Combine",
}
