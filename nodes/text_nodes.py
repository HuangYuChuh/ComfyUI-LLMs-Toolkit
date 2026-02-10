import json
import logging
import string
from typing import Tuple, Dict, Any

# Set up logging
logger = logging.getLogger(__name__)

class SafeFormatter(string.Formatter):
    """
    A custom formatter that leaves missing keys as placeholders
    instead of raising a KeyError.
    Example: "{name} is {age}" with {"name": "Alice"} -> "Alice is {age}"
    """
    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            try:
                return kwargs[key]
            except KeyError:
                return "{" + key + "}"
        return super().get_value(key, args, kwargs)


class StringTemplate:
    """
    Renders a string template using a JSON context.
    
    Inputs:
    - template: The text with variables, e.g., "Hello {name}!"
    - variables: A JSON string containing the variable values.
    
    Returns:
    - string: The formatted string.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {
                    "default": "", 
                    "multiline": True,
                    "dynamicPrompts": False, # Disable standard dynamic prompts to avoid confusion
                    "placeholder": "Enter text here, use {key} for variables..."
                }),
            },
            "optional": {
                "variables": ("STRING", {
                    "default": "{}", 
                    "forceInput": True,
                    "tooltip": "Connect a JSON output (e.g., from JSON Builder) here."
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "render"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Text"
    DESCRIPTION = "Replaces variables in the template string with values from the input JSON variables (e.g. {name}). Missing variables are left as-is."

    def render(self, template: str, variables: str = "{}") -> Tuple[str]:
        # Parse variables
        context = {}
        if variables and variables.strip():
            try:
                context = json.loads(variables)
                if not isinstance(context, dict):
                    logger.warning(f"[StringTemplate] Variables input is not a JSON object, got {type(context)}")
                    context = {} # Fallback to empty if not a dict
            except json.JSONDecodeError as e:
                logger.error(f"[StringTemplate] Failed to parse variables JSON: {e}")
                # Don't fail hard, just use empty context so user sees the template
                context = {}
        
        # Render template
        try:
            formatter = SafeFormatter()
            result = formatter.format(template, **context)
            
            # Log what happened for debugging (geek style)
            replaced_keys = [k for k in context.keys() if "{" + k + "}" in template]
            logger.info(f"[🚦 StringTemplate] Rendered with {len(replaced_keys)} replacements.")
            
            return (result,)
        except Exception as e:
            logger.error(f"[StringTemplate] Error rendering template: {e}")
            return (template,) # Return original on error to be safe


# Register nodes
NODE_CLASS_MAPPINGS = {
    "StringTemplate": StringTemplate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringTemplate": "String Template",
}
