import json
from typing import Tuple


class JSONExtractor:
    """
    Extract value from JSON string by key.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {
                    "multiline": True,
                    "default": "{}"
                }),
                "key": ("STRING", {
                    "default": "",
                    "label": "Key to extract"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)
    FUNCTION = "extract"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/JSON"

    def extract(self, json_string: str, key: str) -> Tuple[str]:
        """
        Extract value from JSON string by key.
        
        Args:
            json_string: JSON string to parse
            key: Key to extract (supports nested keys like 'user.name')
            
        Returns:
            Extracted value as string
        """
        try:
            # Parse JSON string
            data = json.loads(json_string)
            
            # Handle nested keys (e.g., "user.profile.name")
            keys = key.split('.')
            value = data
            
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                    if value is None:
                        return (f"Key '{k}' not found",)
                else:
                    return (f"Cannot access key '{k}' on non-dict value",)
            
            # Convert value to string
            if isinstance(value, (dict, list)):
                result = json.dumps(value, ensure_ascii=False)
            else:
                result = str(value)
            
            print(f"# [🚦 LLMs_Toolkit] extracted {key}={result[:50]}...")
            return (result,)
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON: {str(e)}"
            print(f"# [🚦 LLMs_Toolkit] ✗ {error_msg}")
            return (error_msg,)
        except Exception as e:
            error_msg = f"Extraction error: {str(e)}"
            print(f"# [🚦 LLMs_Toolkit] ✗ {error_msg}")
            return (error_msg,)


# Register the node
NODE_CLASS_MAPPINGS = {"JSONExtractor": JSONExtractor}
NODE_DISPLAY_NAME_MAPPINGS = {"JSONExtractor": "JSON Extractor"}
